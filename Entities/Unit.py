from Entities.Stamina import Stamina


class Unit:
    def __init__(self):
        self.stamina = Stamina()
        self.player_position = None, None

    class OutOfStamina(Exception):
        pass

    def set_position(self, position: tuple):
        self.player_position = position

    def move(self, stamina_cost: int = 1):
        if self.stamina.current_stamina == 0:
            raise self.OutOfStamina
        self.stamina.expend(stamina_cost)

    def start_turn(self):
        self.stamina.reset()



