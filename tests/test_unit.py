import unittest

from Entities.Unit import Unit


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.unit = Unit()

    # Utility
    def unitIsMaxStamina(self) -> bool:
        return self.unit.stamina.max_stamina == self.unit.stamina.current_stamina

    # Tests
    def test_unit_can_set_new_name(self):
        name = "String"
        self.unit.set_name(name)
        self.assertIsNotNone(self.unit.name)

    def test_unit_knows_current_stamina(self):
        self.assertTrue(self.unit.stamina.current_stamina)

    def test_new_unit_has_full_stamina(self):
        self.assertTrue(self.unitIsMaxStamina())

    def test_after_movement_stamina_reduced(self):
        self.unit.move()
        self.assertFalse(self.unitIsMaxStamina())

    def test_when_unit_moves_without_stamina_throws_OutOfStamina(self):
        for i in range(10):
            self.unit.move()
        self.assertRaises(self.unit.OutOfStamina, self.unit.move)

    def test_when_starts_turn_has_max_stamina(self):
        self.unit.current_stamina = 0
        self.unit.start_turn()
        self.assertTrue(self.unitIsMaxStamina())

    def test_unit_can_set_position(self):
        position = (0, 0)
        self.unit.set_position(position)
        self.assertIsNotNone(position[0])
        self.assertIsNotNone(position[1])


if __name__ == '__main__':
    unittest.main()
