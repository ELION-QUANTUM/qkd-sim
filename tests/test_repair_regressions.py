import importlib
import math
import random
import unittest
from unittest.mock import patch

import numpy as np

from q3 import Circuit, StateVectorBackend
from q3.circuits.circuit import Instruction
from q3.communication.qkd import bb84_protocol, qkd_decision
from q3.communication.qkd.attacks import intercept_resend
from q3.communication.qkd.channel import noisy_channel
from q3.core.registers import QubitRef


class Choices:
    def __init__(self, values):
        self.values = iter(values)

    def choice(self, _):
        return next(self.values)


class ProtocolRegressions(unittest.TestCase):
    def test_eve_matching_basis_preserves_each_bit(self):
        for basis in [0, 1]:
            for bit in [0, 1]:
                self.assertEqual(intercept_resend([bit], [basis], Choices([basis, 1-bit])),
                                 ([bit], [basis]))

    def test_eve_opposite_basis_uses_measurement_draw(self):
        for basis in [0, 1]:
            for bit in [0, 1]:
                for draw in [0, 1]:
                    self.assertEqual(intercept_resend([bit], [basis], Choices([1-basis, draw])),
                                     ([draw], [1-basis]))

    def test_bob_remeasures_and_sifts_against_alice(self):
        module = importlib.import_module('q3.communication.qkd.bb84')
        # Alice 0 in basis 1; Eve prepares 0 in basis 0; Bob basis 1 draws 1.
        with patch.object(module.random, 'Random', return_value=Choices([0, 1, 1, 1])), \
             patch.object(module, 'intercept_resend', return_value=([0], [0])):
            report = bb84_protocol(1, attack='intercept_resend')
        self.assertEqual(report['matched_bases'], 1)
        self.assertEqual(report['sifted_bases'], [1])
        self.assertEqual(report['error_rate'], 1)
        # Eve and Bob matching must not retain an Alice/Bob basis mismatch.
        with patch.object(module.random, 'Random', return_value=Choices([0, 1, 0])), \
             patch.object(module, 'intercept_resend', return_value=([0], [0])):
            report = bb84_protocol(1, attack='intercept_resend')
        self.assertEqual(report['matched_bases'], 0)

    def test_empty_sample_is_insufficient(self):
        result = bb84_protocol(n=1, seed=0)
        self.assertEqual(result['matched_bases'], 0)
        self.assertIsNone(result['error_rate'])
        self.assertFalse(result['secure'])
        self.assertEqual(result['threat_level'], 'insufficient_data')
        self.assertEqual(qkd_decision(n=1, seed=0)['threat_level'], 'insufficient_data')

    def test_invalid_public_settings(self):
        cases = [{'n': n} for n in [0, -1, True, 1.5, '2']]
        cases += [{'noise_rate': x} for x in [-0.5, 1.1, math.nan, math.inf, True, '0']]
        cases += [{'attack': x} for x in ['typo', False, []]]
        cases += [{'seed': x} for x in [True, -1, 1.5, '2']]
        cases += [{'thresholds': x} for x in [{}, {'benign_noise_max': math.nan, 'attack_min': .1},
                  {'benign_noise_max': .2, 'attack_min': .1},
                  {'benign_noise_max': .1, 'attack_min': .1},
                  {'benign_noise_max': False, 'attack_min': 1},
                  {'benign_noise_max': 0, 'attack_min': 2}]]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                bb84_protocol(**kwargs)

    def test_probability_boundaries_and_config_copy(self):
        self.assertEqual(noisy_channel([0, 1], 0), [0, 1])
        self.assertEqual(noisy_channel([0, 1], 1), [1, 0])
        self.assertEqual(bb84_protocol(100, noise_rate=0, seed=7)['error_rate'], 0)
        self.assertEqual(bb84_protocol(100, noise_rate=1, seed=7)['error_rate'], 1)
        first = qkd_decision(seed=5)
        first['thresholds_used']['benign_noise_max'] = 1
        self.assertEqual(qkd_decision(seed=5)['thresholds_used']['benign_noise_max'], .03)
        supplied = {'benign_noise_max': 0, 'attack_min': 1}
        self.assertIsNot(qkd_decision(thresholds=supplied)['thresholds_used'], supplied)

    def test_seeded_attack_distribution(self):
        report = bb84_protocol(40000, attack='intercept_resend', seed=123)
        m = report['matched_bases']
        # Sift count Binomial(n, .5); QBER Binomial(m, .25) / m.
        # Six standard deviations give a conservative, justified tolerance.
        self.assertLess(abs(m - 20000), 6 * math.sqrt(40000 * .25))
        self.assertLess(abs(report['error_rate'] - .25), 6 * math.sqrt(.25 * .75 / m))
        self.assertEqual(report, bb84_protocol(40000, attack='intercept_resend', seed=123))


class CircuitRegressions(unittest.TestCase):
    def test_nonterminal_measurement_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'terminal'):
            Circuit(1, num_clbits=2).measure(0, 0).x(0).measure(0, 1).run(shots=10)

    def test_raw_instruction_validation(self):
        invalid = [Instruction('CX', (0,), (0,)), Instruction('H', ()),
                   Instruction('H', (0, 1)), Instruction('H', (0,), (1,)),
                   Instruction('H', (0,), clbit=0), Instruction('CX', (1,)),
                   Instruction('MEASURE', (0,)), Instruction('MEASURE', (0,), (1,), 0),
                   Instruction('TYPO', (0,)), Instruction('H', (True,)),
                   Instruction('H', (.5,)), Instruction('MEASURE', (0,), clbit=True)]
        for instruction in invalid:
            with self.subTest(instruction=instruction), self.assertRaises((ValueError, IndexError)):
                Circuit(2, num_clbits=2).append(instruction)

    def test_backend_revalidates_mutable_instruction_list(self):
        circuit = Circuit(1, num_clbits=1).h(0)
        circuit.instructions.append(Instruction('CX', (0,), (0,)))
        with self.assertRaises(ValueError):
            circuit.run()

    def test_register_ownership_and_type(self):
        a, b = Circuit(), Circuit()
        qa, qb = a.qubits(1), b.qubits(1)
        ca, cb = a.bits(1), b.bits(1)
        a.h(qa[0]).measure(qa[0], ca[0])
        for ref in [qb[0], QubitRef(0), ca[0]]:
            with self.assertRaises(ValueError):
                a.h(ref)
        with self.assertRaises(ValueError):
            a.measure(qa[0], cb[0])

    def test_resource_limit_before_allocation(self):
        with patch.object(StateVectorBackend, '_zero_state', side_effect=AssertionError('allocated')):
            with self.assertRaisesRegex(ValueError, '10 qubits'):
                Circuit(15).h(0).run()

    def test_valid_circuits_preserve_norm_and_terminal_correlations(self):
        circuit = Circuit(3, num_clbits=3).h(0).cx(0, 1).cx(1, 2).z(2).x(2).x(2)
        result = circuit.measure_all().run(shots=128, seed=2)
        self.assertAlmostEqual(float(np.linalg.norm(result.statevector)), 1., places=14)
        self.assertEqual(set(result.counts), {'000', '111'})
        self.assertEqual(sum(result.counts.values()), 128)

    def test_counts_are_positive_integers(self):
        for shots in [0, -1, True, 1.5, '1']:
            with self.subTest(shots=shots), self.assertRaises(ValueError):
                Circuit(1).run(shots=shots)
        for n in [True, -1, 1.5, '2']:
            with self.subTest(n=n), self.assertRaises(ValueError):
                Circuit(num_qubits=n)
