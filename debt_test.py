import unittest
from debt import calculate_interest

class DebtTest(unittest.TestCase):
    def test_interest_calculation(self):
        principal = 3736.13
        interest_charged = 84.31
        days = 32.0
        interest_as_apr = 25.74
        test_interest_charged = calculate_interest(principal, interest_as_apr / 100.0, days / 365.0) - principal
        self.assertAlmostEqual(interest_charged, test_interest_charged, places=2)

if(__name__ == '__main__'):
    unittest.main

