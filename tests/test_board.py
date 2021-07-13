import unittest

from Entities.Board import Board


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def create_new_player(self, position: tuple = (0, 0)):
        self.board.spawn_unit("player", position)
        self.board.set_active_player(self.board.active_player_index)

    def assert_position_exceptions(self, function):
        self.create_new_player()
        self.assertRaises(self.board.PositionOutOfBounds, function, (-1, -1))
        self.assertRaises(self.board.PositionOutOfBounds, function, (-1, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds, function, (self.board.width/2, -1))
        self.assertRaises(self.board.PositionOutOfBounds, function, (self.board.width, self.board.height))
        self.assertRaises(self.board.PositionOutOfBounds, function, (self.board.width, self.board.height/2))
        self.assertRaises(self.board.PositionOutOfBounds, function, (self.board.width/2, self.board.height))

    def is_player_in_different_position(self, start_position: tuple):
        if start_position[0] == self.board.active_player.player_position[0] and \
                start_position[1] == self.board.active_player.player_position[1]:
            return False
        else:
            return True

    def how_much_did_player_stamina_change(self, starting_stamina: int) -> int:
        return starting_stamina - self.board.active_player.stamina.current_stamina

    def take_player_turn(self):
        pass

    # TESTS
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

    def test_when_position_is_out_of_bounds_throws_PositionOutOfBounds(self):
        self.assert_position_exceptions(self.board.get_position)

    def test_PositionOutOfBounds_set(self):
        self.assert_position_exceptions(self.board.set_player_position)

    def test_player_unit_can_be_spawned(self):
        self.assertFalse(self.board.active_player)
        self.board.spawn_unit("player")
        self.assertTrue(len(self.board.player_list) == 1)

    def test_player_unit_position_is_set_when_spawned(self):
        self.create_new_player()
        self.assertIsNotNone(self.board.active_player.player_position[0])
        self.assertIsNotNone(self.board.active_player.player_position[1])

    def test_player_unit_can_set_position(self):
        self.create_new_player()
        self.board.set_player_position((2, 2))
        self.assertEqual(self.board.get_player_position(), (2, 2))

    def test_when_player_position_is_set_out_of_bounds_throws_PositionOutOfBounds(self):
        self.create_new_player()
        self.assertRaises(self.board.PositionOutOfBounds, self.board.set_player_position, (-1, -1))
        self.assertNotEqual(self.board.active_player.player_position[0], -1)
        self.assertNotEqual(self.board.active_player.player_position[1], -1)

    def test_player_unit_moves_onto_adjacent_square(self):
        self.create_new_player()
        start_position = self.board.active_player.player_position
        test_position = self.board.active_player.player_position[0] + 1, self.board.active_player.player_position[1]
        self.board.move_player_unit(test_position)
        self.assertTrue(self.is_player_in_different_position(start_position))
        self.create_new_player()
        start_position = self.board.active_player.player_position
        test_position = self.board.active_player.player_position[0], self.board.active_player.player_position[1] + 1
        self.board.move_player_unit(test_position)
        self.assertTrue(self.is_player_in_different_position(start_position))

    def test_player_moving_out_of_bounds_throws_PositionOutOfBounds(self):
        self.create_new_player()
        test_position = self.board.active_player.player_position[0] - 1, self.board.active_player.player_position[1]
        self.assertRaises(self.board.PositionOutOfBounds, self.board.move_player_unit, test_position)
        test_position = self.board.active_player.player_position[0], self.board.active_player.player_position[1] - 1
        self.assertRaises(self.board.PositionOutOfBounds, self.board.move_player_unit, test_position)

    def test_player_loses_stamina_when_moving(self):
        self.create_new_player()
        starting_stamina = self.board.active_player.stamina.current_stamina
        test_position = self.board.active_player.player_position[0] + 1, self.board.active_player.player_position[1]
        self.board.move_player_unit(test_position)
        self.assertTrue(self.how_much_did_player_stamina_change(starting_stamina))

    def test_player_unit_moving_onto_its_own_tile_throws_InvalidPlayerMovement(self):
        self.create_new_player()
        self.assertRaises(self.board.InvalidPlayerMovement, self.board.move_player_unit, (0, 0))

    def test_player_unit_moving_onto_non_adjacent_tile_throws_InvalidPlayerMovement(self):
        self.create_new_player()
        self.assertRaises(self.board.InvalidPlayerMovement, self.board.move_player_unit, (2, 2))

    def test_player_loses_more_than_one_stamina_when_moving_onto_difficult_terrain(self):
        self.create_new_player()
        self.board.set_active_player(self.board.active_player_index)
        starting_stamina = self.board.active_player.stamina.current_stamina
        self.board.move_player_unit((self.board.active_player.player_position[0] + 1,
                                    self.board.active_player.player_position[1]), 2)
        self.assertEqual(self.how_much_did_player_stamina_change(starting_stamina), 2)

    def test_second_player_can_be_spawned(self):
        self.create_new_player()
        self.assertIsNotNone(self.board.player_list[0])
        self.create_new_player()
        self.assertIsNotNone(self.board.player_list[1])

    def test_active_player_can_be_set(self):
        self.assertIsNone(self.board.active_player)
        self.create_new_player()
        self.board.set_active_player(0)
        self.assertEqual(self.board.active_player, self.board.player_list[0])
        self.create_new_player()
        self.board.set_active_player(1)
        self.assertEqual(self.board.active_player, self.board.player_list[1])

    def test_when_active_player_index_equals_or_exceeds_player_list_length_throws_ActivePlayerIndexOutOfBounds(self):
        self.create_new_player()
        self.assertRaises(self.board.ActivePlayerIndexOutOfBounds, self.board.set_active_player, 1)

    def test_active_player_can_pass_turn_to_next_player(self):
        self.create_new_player()
        self.create_new_player()
        current_player = self.board.active_player
        self.board.pass_turn()
        self.assertNotEqual(current_player, self.board.active_player)

    def test_a_position_is_occupied_when_a_unit_is_on_it(self):
        self.create_new_player()
        self.assertTrue(self.board.is_position_occupied((0, 0)))

    def test_when_spawning_a_second_player_spawns_them_onto_an_unoccupied_position(self):
        self.create_new_player()
        self.assertTrue(self.board.is_position_occupied(self.board.active_player.player_position))
        self.create_new_player()
        self.assertTrue(self.board.is_position_occupied(self.board.active_player.player_position))

    def test_when_spawning_a_player_on_a_position_out_of_bounds_throws_PositionOutOfBounds(self):
        self.assertRaises(self.board.PositionOutOfBounds, self.board.spawn_unit, "player", (-1, -1))

    def test_when_a_player_sets_position_to_an_occupied_position_throws_PositionAlreadyOccupied(self):
        self.create_new_player()
        test_position = self.board.active_player.player_position
        self.create_new_player()
        self.assertRaises(self.board.PositionAlreadyOccupied, self.board.set_player_position, test_position)

    def test_all_players_can_take_a_turn(self):
        for i in range(4):
            self.create_new_player()
        for i in range(4):
            self.assertEqual(i, self.board.active_player_index)
            self.board.pass_turn()
        self.assertEqual(0, self.board.active_player_index)

    def test_enemy_unit_can_be_spawned(self):
        self.board.spawn_unit("enemy")
        self.assertTrue(len(self.board.enemy_list) == 1)


if __name__ == '__main__':
    unittest.main()
