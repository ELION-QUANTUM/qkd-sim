import math
import unittest

import numpy as np

from q3.circuits import Circuit
from q3.core.gates import H, X, Z
from q3.simulator import StateVectorBackend


class Q3CoreTests(unittest.TestCase):
    def test_gate_matrices(self):
        expected_h = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        np.testing.assert_allclose(H, expected_h)
        np.testing.assert_allclose(X, np.array([[0, 1], [1, 0]], dtype=complex))
        np.testing.assert_allclose(Z, np.array([[1, 0], [0, -1]], dtype=complex))

    def test_bell_state_amplitudes(self):
        circuit = Circuit(num_qubits=2, num_clbits=2)
        circuit.h(0).cx(0, 1).measure_all()

        result = StateVectorBackend(seed=1).run(circuit, shots=256)
        expected = np.array(
            [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)],
            dtype=complex,
        )
        np.testing.assert_allclose(result["statevector"], expected, atol=1e-9)

    def test_measurement_counts_for_x_gate(self):
        circuit = Circuit(num_qubits=1, num_clbits=1)
        circuit.x(0).measure(0, 0)

        result = StateVectorBackend(seed=2).run(circuit, shots=256)
        self.assertEqual(result["counts"], {"1": 256})

    def test_invalid_qubit_index_raises(self):
        circuit = Circuit(num_qubits=1, num_clbits=1)
        with self.assertRaises(IndexError):
            circuit.h(3)


if __name__ == "__main__":
    unittest.main()
