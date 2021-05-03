
"""This module contains functions to apply the quantum phase estimation
algorithm.
"""
import typing
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
from hhl4x4.utils.endianness import QRegisterBE
from hhl4x4.custom_gates.qft import iqft_be

import hhl4x4.custom_gates.comment

QubitType = typing.Tuple[QuantumRegister, int]


class QuantumPhaseEstimationGate(CompositeGate):

    def __init__(self, phase_quantum_register, eigenvector_quantum_register,
                 controlled_hamiltonian_powers, precision: float = 0.1,
                 qcirc=None):
        """Initialize the QuantumPhaseEstimationGate class.

        Apply the Quantum Phase Estimation algorithm to estimate the eigenvalue
        phase and store it in big-endian in phase_quantum_register.

        :param phase_quantum_register: 0>^n state in input, stores the
        approximation of the eigenvalue phase at the end of the algorithm.
        :param eigenvector_quantum_register: |psi> state, an eigenvector of U,
        in input, the same state in output.
        :param controlled_hamiltonian_powers: A callable that implements the
        quantum circuits
        applying the controlled-U^{2^i} transformations.
        c_U_powers(i, circuit, control, quantum_register) applies U^{2^i} on
        'quantum_register', controlled by the qubit 'control'.
        :param precision:
        :param qcirc: The associated quantum circuit.
        """

        n, m = len(phase_quantum_register), len(eigenvector_quantum_register)
        phase_qubits = [phase_quantum_register[i] for i in range(n)]
        eigenvector_qubits = [eigenvector_quantum_register[i] for i in range(m)]
        used_qubits = phase_qubits + eigenvector_qubits

        super().__init__(self.__class__.__name__,  # name
                         [],  # parameters
                         used_qubits,  # qubits
                         qcirc)  # circuit

        self.comment("[QPE] Starting block.")
        self.comment("[QPE] 1. Hadamard gate.")
        self.h(phase_quantum_register)
        self.comment("[QPE] 2. Phase estimation.")
        for i in range(n):
            self.comment(
                "[QPE] 2.{0}. Start of step {0} of phase estimation.".format(i))
            controlled_hamiltonian_powers(i, self,
                                          phase_quantum_register[n - 1 - i],
                                          eigenvector_quantum_register)
            self.comment(
                "[QPE] 2.{0}. End of step {0} of phase estimation.".format(i))

        self.comment("[QPE] 3. Inverse QFT.")
        iqft_be(self, phase_quantum_register, qcirc)
        self.comment("[QPE] End block.")


def qpe(self, phase_quantum_register: QRegisterBE,
        eigenvector_quantum_register: QRegisterBE,
        controlled_hamiltonian_powers: typing.Callable[
            [int, CompositeGate, QubitType, QRegisterBE], None],
        precision: float = 0.1) -> QuantumPhaseEstimationGate:
    self._check_qreg(phase_quantum_register)
    self._check_qreg(eigenvector_quantum_register)
    self._check_dups([phase_quantum_register, eigenvector_quantum_register])
    return self._attach(QuantumPhaseEstimationGate(phase_quantum_register,
                                                   eigenvector_quantum_register,
                                                   controlled_hamiltonian_powers,
                                                   precision, self))


QuantumCircuit.qpe = qpe
CompositeGate.qpe = qpe
