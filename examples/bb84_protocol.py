from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3.communication.qkd import bb84_protocol, qkd_decision


def print_report(title, report):
    print(title)
    print(f"Raw bits sent:         {report['raw_bits']}")
    print(f"Matched bases:         {report['matched_bases']}")
    print(f"Final key length:      {report['final_key_length']}")
    print(f"Error rate (QBER):     {report['error_rate']:.4f}")
    print(f"Secure channel:        {report['secure']}")
    print(f"Threat level:          {report['threat_level']}")
    print(f"Threat reason:         {report['threat_reason']}")
    print(f"Post-processing:       {report['postprocessing']}")
    print("")


def print_decision(title, decision):
    print(title)
    print(f"Secure:                {decision['secure']}")
    print(f"Threat level:          {decision['threat_level']}")
    print(f"Error rate (QBER):     {decision['error_rate']:.4f}")
    print(f"Thresholds used:       {decision['thresholds_used']}")
    print("")


def main():
    report = bb84_protocol(1000, seed=5)
    print_report("=== BB84 Report (No attack, No noise) ===", report)

    decision = qkd_decision(1000, seed=5)
    print_decision("=== BB84 Decision (No attack, No noise) ===", decision)

    report_attack = bb84_protocol(1000, attack="intercept_resend", seed=5)
    print_report("=== BB84 Report (Intercept-Resend) ===", report_attack)


if __name__ == "__main__":
    main()
