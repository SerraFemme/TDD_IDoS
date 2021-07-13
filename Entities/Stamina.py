SMALLEST_MAXIMUM: int = 1
DEFAULT_MAXIMUM: int = 10
LARGEST_MAXIMUM: int = 2 * DEFAULT_MAXIMUM


class Stamina:
    def __init__(self, default_max: int = DEFAULT_MAXIMUM):
        self.default_max: int = default_max
        self.max_stamina: int = default_max
        self.current_stamina: int = self.max_stamina

    class NotEnoughStamina(Exception):
        pass

    class StaminaFull(Exception):
        pass

    class StaminaExceedsMax(Exception):
        pass

    class StaminaMaxRecedesOne(Exception):
        pass

    class StaminaMaxExceedsTwenty(Exception):
        pass

    def expend(self, amount: int):
        if self.current_stamina < amount:
            raise self.NotEnoughStamina
        self.current_stamina -= amount

    def reset(self):
        self.current_stamina = self.max_stamina

    def recover(self, amount: int):
        if self.current_stamina == self.max_stamina:
            raise self.StaminaFull
        elif self.current_stamina + amount > self.max_stamina:
            raise self.StaminaExceedsMax
        self.current_stamina += amount

    def set_max(self, new_max):
        if new_max < SMALLEST_MAXIMUM:
            raise self.StaminaMaxRecedesOne
        elif new_max > LARGEST_MAXIMUM:
            raise self.StaminaMaxExceedsTwenty
        self.max_stamina = new_max
        if self.current_stamina > self.max_stamina:
            self.current_stamina = self.max_stamina
        
    def reset_max(self):
        self.max_stamina = self.default_max
