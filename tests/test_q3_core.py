import math
import unittest

import numpy as np

from q3 import Circuit, RunResult
from q3.circuits import Circuit as CircuitDirect
from q3.core.gates import H, X, Z
from q3.core.registers import BitRef, QubitRef
from q3.simulator import StateVectorBackend


class Q3CoreTests(unittest.TestCase):
    def test_public_api_exports(self):
        self.assertIs(Circuit, CircuitDirect)

    def test_register_allocation_returns_typed_refs(self):
        circuit = Circuit("typed_registers")
        q = circuit.qubits(2)
        c = circuit.bits(2)

        self.assertIsInstance(q[0], QubitRef)
        self.assertIsInstance(c[0], BitRef)

    def test_gate_matrices(self):
        expected_h = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        np.testing.assert_allclose(H, expected_h)
        np.testing.assert_allclose(X, np.array([[0, 1], [1, 0]], dtype=complex))
        np.testing.assert_allclose(Z, np.array([[1, 0], [0, -1]], dtype=complex))

    def test_bell_state_amplitudes(self):
        circuit = Circuit("bell")
        q = circuit.qubits(2)
        m = circuit.bits(2)
        circuit.h(q[0]).cx(q[0], q[1]).measure(q[0], m[0]).measure(q[1], m[1])

        result = StateVectorBackend(seed=1).run(circuit, shots=256)
        self.assertIsInstance(result, RunResult)
        expected = np.array(
            [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)],
            dtype=complex,
        )
        np.testing.assert_allclose(result.statevector, expected, atol=1e-9)

    def test_measurement_counts_for_x_gate(self):
        circuit = Circuit("x_gate")
        q = circuit.qubits(1)
        c = circuit.bits(1)
        circuit.x(q[0]).measure(q[0], c[0])

        result = StateVectorBackend(seed=2).run(circuit, shots=256)
        self.assertEqual(result.counts, {"1": 256})

    def test_invalid_qubit_index_raises(self):
        circuit = Circuit(num_qubits=1, num_clbits=1)
        with self.assertRaises(IndexError):
            circuit.h(3)

    def test_repeated_register_allocation_raises(self):
        circuit = Circuit("duplicate_register")
        circuit.qubits(1)
        with self.assertRaises(ValueError):
            circuit.qubits(1)


if __name__ == "__main__":
    unittest.main()
