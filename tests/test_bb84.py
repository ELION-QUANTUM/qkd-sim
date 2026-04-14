import unittest

from q3.communication.qkd import bb84_protocol
from qkd import qkd_decision


class BB84ProtocolTests(unittest.TestCase):
    def test_deterministic_bb84_with_seed(self):
        report_one = bb84_protocol(2000, noise_rate=0.01, seed=42)
        report_two = bb84_protocol(2000, noise_rate=0.01, seed=42)

        self.assertEqual(report_one["error_rate"], report_two["error_rate"])
        self.assertEqual(report_one["threat_level"], report_two["threat_level"])

    def test_autonomy_decision_deterministic(self):
        decision_one = qkd_decision(3000, attack="intercept_resend", seed=123)
        decision_two = qkd_decision(3000, attack="intercept_resend", seed=123)

        self.assertEqual(decision_one, decision_two)


if __name__ == "__main__":
    unittest.main()
