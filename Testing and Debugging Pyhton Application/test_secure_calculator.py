import unittest
from secure_calculator import SecureCalculator

class TestSecureCalculator0452(unittest.TestCase):
    def setUp(self):
        self.calc = SecureCalculator()

    def test_addition(self):
        self.assertEqual(self.calc.add("6", "4"), 10)
        self.assertEqual(self.calc.add("11", "-3"), 8)

    def test_subtraction(self):
        self.assertEqual(self.calc.subtract("11", "4"), 7)
        self.assertEqual(self.calc.subtract("11", "-4"), 15)

    def test_multiplication(self):
        self.assertEqual(self.calc.multiply("5", "6"), 30)
        self.assertEqual(self.calc.multiply("-5", "6"), -30)

    def test_division(self):
        self.assertEqual(self.calc.divide("12", "3"), 4)
        self.assertEqual(self.calc.divide("10", "5"), 2)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide("10", "0")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.add("abcef", "35")

if __name__ == '__main__':
    unittest.main()
