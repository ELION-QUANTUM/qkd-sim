from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3.circuits import Circuit
from q3.simulator import StateVectorBackend


def main() -> None:
    circuit = Circuit(num_qubits=2, num_clbits=2)
    circuit.h(0).cx(0, 1).measure_all()

    result = StateVectorBackend(seed=7).run(circuit, shots=2048)

    print("Bell-state counts")
    for bitstring, count in sorted(result["counts"].items()):
        print(f"{bitstring}: {count}")
    print("")
    print("Statevector:")
    print(result["statevector"])


if __name__ == "__main__":
    main()
