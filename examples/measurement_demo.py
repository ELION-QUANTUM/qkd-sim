from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3.circuits import Circuit
from q3.simulator import StateVectorBackend


def main() -> None:
    circuit = Circuit(num_qubits=1, num_clbits=1)
    circuit.h(0).measure(0, 0)

    result = StateVectorBackend(seed=11).run(circuit, shots=1000)

    print("Measurement demo for H|0>")
    print("Counts:", result["counts"])
    print("Memory sample:", result["memory"][:10])


if __name__ == "__main__":
    main()
