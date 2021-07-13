from Entities.Unit import Unit

BOARD_MINIMUM: int = 4
BOARD_MAXIMUM: int = 50
BOARD_DEFAULT: int = 10


class Board:
    def __init__(self, width: int = BOARD_DEFAULT, height: int = BOARD_DEFAULT):
        if not BOARD_MINIMUM < width <= BOARD_MAXIMUM or not BOARD_MINIMUM < height <= BOARD_MAXIMUM:
            raise self.InvalidBoardSize
        self.width = width
        self.height = height
        self.player_list = []
        self.enemy_list = []
        self.active_player: Unit() = None
        self.active_enemy: Unit() = None
        self.active_player_index: int = 0
        # self.enemy_unit = None

    class InvalidBoardSize(Exception):
        pass

    class PositionOutOfBounds(Exception):
        pass

    class InvalidPlayerMovement(Exception):
        pass

    class ActivePlayerIndexOutOfBounds(Exception):
        pass

    class PositionAlreadyOccupied(Exception):
        pass

    def get_position(self, position: tuple) -> tuple:
        if not (0 <= position[0] < self.width and 0 <= position[1] < self.height):
            raise self.PositionOutOfBounds
        return position

    def spawn_unit(self, unit_type: str, position: tuple = (0, 0)):
        new_unit = Unit()
        if not self.is_position_occupied(position):
            self.set_player_position(position, new_unit)
        if unit_type == "player":
            self.player_list.append(new_unit)
        else:
            self.enemy_list.append(new_unit)

    def set_player_position(self, position: tuple, player: Unit = None):
        if not (0 <= position[0] < self.width and 0 <= position[1] < self.height):
            raise self.PositionOutOfBounds
        if self.is_position_occupied(position):
            raise self.PositionAlreadyOccupied
        if player is None:
            self.active_player.set_position(position)
        else:
            player.set_position(position)

    def get_player_position(self) -> tuple:
        return self.active_player.player_position

    def move_player_unit(self, position: tuple, stamina_cost: int = 1):
        x = position[0]
        y = position[1]
        if abs((x + y) - (self.active_player.player_position[0] + self.active_player.player_position[1])) != 1 \
                or self.active_player.player_position[0] + self.active_player.player_position[1] == x + y:
            raise self.InvalidPlayerMovement
        self.set_player_position(position)
        self.active_player.move(stamina_cost)

    def pass_turn(self):
        self.active_player_index += 1
        if self.active_player_index >= len(self.player_list):
            self.active_player_index = 0
        self.set_active_player(self.active_player_index)
        self.active_player.start_turn()

    def set_active_player(self, active_index):
        if active_index >= len(self.player_list):
            raise self.ActivePlayerIndexOutOfBounds
        self.active_player = self.player_list[active_index]

    def is_position_occupied(self, position: tuple) -> bool:
        x = position[0]
        y = position[1]
        for player in self.player_list:
            if x == player.player_position[0] and y == player.player_position[1]:
                return True
        return False
