from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3.communication.qkd import qkd_decision


def run_noise_sweep(
    n=3000,
    noise_levels=None,
    runs_per_level=5,
    seed_base=1000,
):
    if noise_levels is None:
        noise_levels = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05]

    results = []

    for noise in noise_levels:
        for run in range(runs_per_level):
            seed = seed_base + run
            decision = qkd_decision(
                n=n,
                noise_rate=noise,
                seed=seed,
            )

            results.append({
                "noise_rate": noise,
                "run": run,
                "error_rate": decision["error_rate"],
                "threat_level": decision["threat_level"],
                "secure": decision["secure"],
                "seed": seed,
            })

    return results


def print_results(results):
    print("noise_rate,run,error_rate,threat_level,secure,seed")
    for r in results:
        print(
            f"{r['noise_rate']},"
            f"{r['run']},"
            f"{r['error_rate']:.4f},"
            f"{r['threat_level']},"
            f"{r['secure']},"
            f"{r['seed']}"
        )


if __name__ == "__main__":
    results = run_noise_sweep()
    print_results(results)
