from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3.circuits import Circuit
from q3.simulator import StateVectorBackend


def main() -> None:
    circuit = Circuit(num_qubits=1, num_clbits=1)
    circuit.x(0).measure(0, 0)

    result = StateVectorBackend(seed=21).run(circuit, shots=256)

    print("Single-qubit X gate example")
    print("Counts:", result["counts"])
    print("Statevector:", result["statevector"])


if __name__ == "__main__":
    main()
