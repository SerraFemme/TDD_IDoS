import unittest

from Entities import Stamina


class StaminaTest(unittest.TestCase):
    def setUp(self):
        self.stamina = Stamina(10)

    def is_max_stamina(self) -> bool:
        return self.stamina.current_stamina == self.stamina.max_stamina

    def test_stamina_has_current_value(self):
        self.assertTrue(self.stamina.current_stamina)

    def test_stamina_is_initiated_at_max(self):
        self.assertTrue(self.is_max_stamina())

    def test_stamina_can_change_current_value(self):
        self.stamina.expend(10)
        self.assertFalse(self.is_max_stamina())

    def test_expend_stamina_when_zero_throws_NotEnoughStamina_exception(self):
        self.stamina.expend(10)
        self.assertRaises(Stamina.NotEnoughStamina, self.stamina.expend, 1)

    def test_current_stamina_can_be_reset_to_max(self):
        self.stamina.expend(10)
        self.stamina.reset()
        self.assertTrue(self.is_max_stamina())

    def test_recover_at_full_stamina_throws_StaminaFull(self):
        self.assertRaises(self.stamina.StaminaFull, self.stamina.recover, 1)

    def test_stamina_can_be_expended(self):
        self.stamina.expend(1)
        self.assertEqual(self.stamina.current_stamina, self.stamina.max_stamina-1)

    def test_stamina_can_be_recovered(self):
        self.stamina.expend(1)
        self.assertEqual(self.stamina.current_stamina, self.stamina.max_stamina-1)
        self.stamina.recover(1)
        self.assertEqual(self.stamina.current_stamina, self.stamina.max_stamina)

    def test_when_stamina_recovers_past_max_when_not_at_max_throws_StaminaExceedsMax(self):
        self.stamina.expend(1)
        self.assertRaises(self.stamina.StaminaExceedsMax, self.stamina.recover, 2)

    def test_stamina_max_altered(self):
        self.stamina.set_max(5)
        self.assertEqual(self.stamina.max_stamina, 5)

    def test_stamina_max_can_be_reset_to_default(self):
        self.stamina.set_max(5)
        self.assertEqual(self.stamina.max_stamina, 5)
        self.stamina.reset_max()
        self.assertEqual(self.stamina.max_stamina, 10)

    def test_when_stamina_max_is_set_below_one_throws_StaminaMaxRecedesOne(self):
        self.assertRaises(self.stamina.StaminaMaxRecedesOne, self.stamina.set_max, 0)

    def test_when_stamina_max_is_set_above_twenty_throws_StaminaMaxExceedsTwenty(self):
        self.assertRaises(self.stamina.StaminaMaxExceedsHardCap, self.stamina.set_max, 21)

    def test_when_stamina_max_is_set_below_current_value_set_current_value_to_max(self):
        self.stamina.set_max(5)
        self.assertTrue(self.is_max_stamina())


if __name__ == '__main__':
    unittest.main()
