import unittest

from qkd import qkd_decision


class AutonomyApiTests(unittest.TestCase):
    def test_qkd_decision_minimal_keys(self):
        decision = qkd_decision(n=500)

        self.assertIsInstance(decision, dict)
        self.assertEqual(
            set(decision.keys()),
            {"secure", "threat_level", "error_rate", "thresholds_used"},
        )

    def test_qkd_decision_attack_flags(self):
        decision = qkd_decision(n=3000, attack="intercept_resend", seed=9)

        self.assertFalse(decision["secure"])
        self.assertEqual(decision["threat_level"], "suspected_attack")

    def test_qkd_decision_noise_typically_ok(self):
        decision = qkd_decision(n=3000, noise_rate=0.01, seed=9)

        self.assertEqual(decision["threat_level"], "benign_noise")


if __name__ == "__main__":
    unittest.main()
