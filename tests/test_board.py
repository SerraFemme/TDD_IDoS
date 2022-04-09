import unittest

from Entities.Board import Board
from Entities.Unit import Unit

player_spawn_position: tuple = (0, 0)
enemy_spawn_position: tuple = None

player_team_name = "Team_Players"
enemy_team_name = "Team_Enemies"


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.create_team(player_team_name)
        self.board.create_team(enemy_team_name)
        self.enemy_spawn_position = self.board.width-1, self.board.height-1

    # Utility Functions
    def is_unit_in_different_position(self, unit: Unit, start_position: tuple):
        if start_position[0] == unit.position[0] and start_position[1] == unit.position[1]:
            return False
        else:
            return True

    def how_much_did_unit_stamina_change(self, unit: Unit, starting_stamina: int) -> int:
        return starting_stamina - unit.stamina.current_stamina

    def take_player_turn(self):
        pass

    # Board Tests
    def test_new_board(self):
        self.assertTrue(self.board.width)
        self.assertTrue(self.board.height)

    def test_new_board_can_set_initial_size(self):
        self.board = Board(15, 15)
        self.assertTrue(self.board.width == 15)
        self.assertTrue(self.board.height == 15)

    def test_when_board_size_is_set_to_invalid_size_throws_InvalidBoardSize(self):
        self.assertRaises(self.board.InvalidBoardSize, Board, 0, 0)
        self.assertRaises(self.board.InvalidBoardSize, Board, 51, 51)

    def test_board_has_positions(self):
        self.assertTrue(self.board.get_position((0, 0)))

    def test_board_getting_invalid_position_throws_PositionOutOfBounds(self):
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (-1, -1))
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (-1, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (self.board.width/2, -1))
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (self.board.width, self.board.height))
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (self.board.width, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds,
                          self.board.get_position, (self.board.width/2, self.board.height))

    def test_board_setting_invalid_unit_position_throws_PositionOutOfBounds(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        test_unit = player_team.get_active_unit()

        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (-1, -1))
        self.assertNotEqual(test_unit.position[0], -1)
        self.assertNotEqual(test_unit.position[1], -1)
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (-1, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (self.board.width/2, -1))
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (self.board.width, self.board.height))
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (self.board.width, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_unit_position,
                          test_unit, (self.board.width/2, self.board.height))

    # Team Tests
    def test_creating_a_team_with_the_same_name_as_an_existing_one_throws_TeamNameAlreadyTaken(self):
        self.assertRaises(self.board.TeamNameAlreadyTaken, self.board.create_team, player_team_name)

    def test_team_empty_unit_list_throws_UnitListEmpty(self):
        for team in self.board.team_dict:
            self.assertRaises(self.board.team_dict[team].UnitListEmpty, self.board.team_dict[team].get_active_unit)

    # Game Unit Tests
    def test_unit_can_be_spawned(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        self.assertIsNotNone(player_team.get_active_unit())

        enemy_team = self.board.team_dict[enemy_team_name]
        enemy_team.spawn_unit()
        self.assertIsNotNone(enemy_team.get_active_unit())

    def test_unit_can_set_position(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, (2, 2))
        self.assertEqual(player_unit.position, (2, 2))

        enemy_team = self.board.team_dict[enemy_team_name]
        enemy_team.spawn_unit()
        enemy_unit = enemy_team.get_active_unit()
        self.board.set_unit_position(enemy_unit, (5, 5))
        self.assertEqual(enemy_unit.position, (5, 5))

    def test_player_unit_moves_onto_adjacent_square(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)
        test_positions = [(player_unit.position[0]+1, player_unit.position[1]),
                          (player_unit.position[0]+1, player_unit.position[1]+1)]
        for i in range(len(test_positions)):
            start_position = player_unit.position
            self.board.move_unit(player_unit, test_positions[i])
            self.assertTrue(self.is_unit_in_different_position(player_unit, start_position))

    def test_player_moving_out_of_bounds_throws_PositionOutOfBounds(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)

        test_position = player_unit.position[0] - 1, player_unit.position[1]
        self.assertRaises(self.board.PositionOutOfBounds, self.board.move_unit, player_unit, test_position)
        test_position = player_unit.position[0], player_unit.position[1] - 1
        self.assertRaises(self.board.PositionOutOfBounds, self.board.move_unit, player_unit, test_position)

    def test_player_loses_stamina_when_moving(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)

        starting_stamina = player_unit.stamina.current_stamina
        test_position = player_unit.position[0] + 1, player_unit.position[1]
        self.board.move_unit(player_unit, test_position)
        self.assertTrue(self.how_much_did_unit_stamina_change(player_unit, starting_stamina))

    def test_player_unit_moving_onto_its_own_tile_throws_InvalidPlayerMovement(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)
        self.assertRaises(self.board.InvalidUnitMovement, self.board.move_unit, player_unit, player_spawn_position)

    def test_player_unit_moving_onto_non_adjacent_tile_throws_InvalidPlayerMovement(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)
        self.assertRaises(self.board.InvalidUnitMovement, self.board.move_unit, player_unit, (2, 2))

    def test_player_loses_more_than_one_stamina_when_moving_onto_difficult_terrain(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)

        starting_stamina = player_unit.stamina.current_stamina
        test_position = (player_unit.position[0] + 1, player_unit.position[1])
        self.board.move_unit(player_unit, test_position, 2)
        self.assertEqual(self.how_much_did_unit_stamina_change(player_unit, starting_stamina), 2)

    def test_second_player_can_be_spawned(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit("One")
        player_team.spawn_unit("Two")
        self.assertEqual(len(player_team.unit_list), 2)

    def test_when_active_player_index_equals_or_exceeds_player_list_length_throws_ActivePlayerIndexOutOfBounds(self):
        player_team = self.board.team_dict[player_team_name]
        self.assertRaises(player_team.ActiveUnitIndexOutOfBounds, player_team.set_active_unit_index, 1)

    def test_active_player_can_pass_turn_to_next_player(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_team.spawn_unit()
        starting_index = player_team.active_unit_index
        player_team.pass_unit_turn()
        self.assertNotEqual(starting_index, player_team.active_unit_index)

    def test_a_position_is_occupied_when_a_unit_is_on_it(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit()
        player_unit = player_team.get_active_unit()
        self.board.set_unit_position(player_unit, player_spawn_position)
        self.assertTrue(self.board.is_position_occupied((0, 0)))

    def test_when_a_player_sets_position_to_an_occupied_position_throws_PositionAlreadyOccupied(self):
        player_team = self.board.team_dict[player_team_name]
        player_team.spawn_unit("One")
        player_team.spawn_unit("Two")

        self.board.set_unit_position(player_team.get_unit("One"), player_spawn_position)
        self.assertRaises(self.board.PositionAlreadyOccupied, self.board.set_unit_position,
                          player_team.get_unit("Two"), player_spawn_position)

    def test_all_players_can_take_a_turn(self):
        player_team = self.board.team_dict[player_team_name]
        for i in range(4):
            player_team.spawn_unit()

        for i in range(4):
            self.assertEqual(i, player_team.active_unit_index)
            player_team.pass_unit_turn()

    def test_board_can_set_active_team(self):
        self.board.set_active_team(enemy_team_name)
        self.assertEqual(self.board.get_active_team(), enemy_team_name)
        self.board.set_active_team(player_team_name)
        self.assertEqual(self.board.get_active_team(), player_team_name)

    def test_setting_a_nonexistent_team_active_throwsTeamDoesNotExist(self):
        self.assertRaises(self.board.TeamDoesNotExist, self.board.set_active_team, "Test")

    def test_player_team_passes_to_enemy_team_when_all_players_have_taken_their_turn(self):
        player_team = self.board.team_dict[player_team_name]
        enemy_team = self.board.team_dict[enemy_team_name]
        for i in range(4):
            player_team.spawn_unit()
        self.assertEqual(self.board.get_active_team(), player_team_name)
        self.assertNotEqual(self.board.get_active_team(), enemy_team_name)

        player_team.pass_unit_turn()
        self.assertEqual(self.board.get_active_team(), player_team_name)
        player_team.pass_unit_turn()
        self.assertEqual(self.board.get_active_team(), player_team_name)
        player_team.pass_unit_turn()
        self.assertEqual(self.board.get_active_team(), player_team_name)
        player_team.pass_unit_turn()
        self.assertNotEqual(self.board.get_active_team(), player_team_name)  # SJB Here
        self.assertEqual(self.board.get_active_team(), enemy_team_name)


if __name__ == '__main__':
    unittest.main()
