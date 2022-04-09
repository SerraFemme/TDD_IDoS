from Entities.Unit import Unit

BOARD_MINIMUM: int = 4
BOARD_MAXIMUM: int = 50
BOARD_DEFAULT: int = 10


class Board:
    def __init__(self, new_width: int = BOARD_DEFAULT, new_height: int = BOARD_DEFAULT):
        if not BOARD_MINIMUM < new_width <= BOARD_MAXIMUM or not BOARD_MINIMUM < new_height <= BOARD_MAXIMUM:
            raise self.InvalidBoardSize
        self.width = new_width
        self.height = new_height

        self.team_dict: Team() = {}
        self.active_team: str = None

    class InvalidBoardSize(Exception):
        pass

    class PositionOutOfBounds(Exception):
        pass

    class InvalidUnitMovement(Exception):
        pass

    class PositionAlreadyOccupied(Exception):
        pass

    class TeamNameAlreadyTaken(Exception):
        pass

    class TeamDoesNotExist(Exception):
        pass

    class TeamInactive(Exception):
        pass

    # Teams
    def create_team(self, team_name: str):
        if self.does_team_exist(team_name):
            raise self.TeamNameAlreadyTaken
        else:
            self.team_dict[team_name] = Team()

        if self.active_team is None:
            self.active_team = team_name

    def does_team_exist(self, team_name: str):
        if team_name in self.team_dict:
            return True
        return False

    def get_active_team(self) -> str:
        return self.active_team

    def set_active_team(self, team_name: str):
        if self.does_team_exist(team_name):
            self.active_team = team_name
        else:
            raise self.TeamDoesNotExist

    # Positions
    def get_position(self, position: tuple) -> tuple:
        if not (0 <= position[0] < self.width and 0 <= position[1] < self.height):
            raise self.PositionOutOfBounds
        return position

    def set_unit_position(self, unit: Unit, position: tuple):
        if not (0 <= position[0] < self.width and 0 <= position[1] < self.height):
            raise self.PositionOutOfBounds
        if self.is_position_occupied(position):
            raise self.PositionAlreadyOccupied
        unit.set_position(position)

    def move_unit(self, unit: Unit, position: tuple, stamina_cost: int = 1):
        x = position[0]
        y = position[1]
        if abs((x + y) - (unit.position[0] + unit.position[1])) != 1 \
                or unit.position[0] + unit.position[1] == x + y:
            raise self.InvalidUnitMovement
        self.set_unit_position(unit, position)
        unit.move(stamina_cost)

    def is_position_occupied(self, position: tuple) -> bool:
        x = position[0]
        y = position[1]
        for team in self.team_dict:
            for unit in self.team_dict[team].unit_list:
                if x == unit.position[0] and y == unit.position[1]:
                    return True
        return False

    def validate_spawn_position(self, position: tuple, unit: str = "player") -> tuple:
        if self.is_position_occupied(position):
            if unit == "player":
                for j in range(self.height):
                    for i in range(self.width):
                        if not self.is_position_occupied((i, j)):
                            return i, j
                raise self.PositionAlreadyOccupied
            else:
                for j in range(self.height-1, 0, -1):
                    for i in range(self.width-1, 0, -1):
                        if not self.is_position_occupied((i, j)):
                            return i, j
                raise self.PositionAlreadyOccupied
        else:
            return position


class Team:
    def __init__(self):
        self.unit_list = []
        self.active_team: bool = False
        self.active_unit_index: int = -1

    class ActiveUnitIndexOutOfBounds(Exception):
        pass

    class CannotPassUnitTurn(Exception):
        pass

    class UnitListEmpty(Exception):
        pass

    class NamedUnitDoesNotExist(Exception):
        pass

    # Team Functions
    def set_active_unit_index(self, active_index):
        if active_index >= len(self.unit_list) or active_index < 0:
            raise self.ActiveUnitIndexOutOfBounds
        self.active_unit_index = active_index

    def spawn_unit(self, unit_name: str = None):
        new_unit = Unit(unit_name)
        self.unit_list.append(new_unit)
        if self.active_unit_index is -1:
            self.active_unit_index = 0

    def pass_unit_turn(self):
        if len(self.unit_list) > 0:
            if self.active_unit_index < len(self.unit_list)-1:
                self.set_active_unit_index(self.active_unit_index+1)
            elif self.active_unit_index == len(self.unit_list)-1:
                self.set_active_unit_index(0)
            else:
                raise self.CannotPassUnitTurn
            unit = self.get_active_unit()
            unit.start_turn()
        else:
            raise self.UnitListEmpty

        self.unit_list[self.active_unit_index].start_turn()

    def get_active_unit(self) -> Unit:
        if len(self.unit_list) > 0:
            return self.unit_list[self.active_unit_index]
        else:
            raise self.UnitListEmpty

    def get_unit(self, name: str) -> Unit:
        for unit in self.unit_list:
            if unit.name is name:
                return unit
        raise self.NamedUnitDoesNotExist
