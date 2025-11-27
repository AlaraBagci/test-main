import unittest
from analytics import calculate_risk

class TestRiskLogic(unittest.TestCase):
    def test_high_stress_risk(self):
        # Stress > 4 is Critical
        result = calculate_risk(avg_stress=4.5, avg_sleep=7)
        self.assertEqual(result['status'], "Critical")

    def test_low_sleep_risk(self):
        # Sleep < 5 is Warning
        result = calculate_risk(avg_stress=2, avg_sleep=4)
        self.assertEqual(result['status'], "Warning")

if __name__ == '__main__':
    unittest.main()