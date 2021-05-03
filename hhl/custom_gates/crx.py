
"""This module contains functions to apply a controlled-Rx gate.
"""
from typing import Tuple
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
import hhl4x4.custom_gates.comment
import hhl4x4.custom_gates.crzz
from sympy import pi

QubitType = Tuple[QuantumRegister, int]


class CRxGate(CompositeGate):

    def __init__(self, theta: float, ctrl: QubitType, target: QubitType,
                 circuit: QuantumCircuit = None):
        """Initialize the CRxGate class.

        :param theta: Phase added to the quantum state of qubit.
        :param ctrl: The control qubit used to control the Rx gate.
        :param target: The qubit on which the Rx gate is applied.
        :param circuit: The associated quantum circuit.
        """
        used_qubits = [ctrl, target]

        super().__init__(self.__class__.__name__,  # name
                         [theta],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit

        self.comment("c-RX")
        # Apply the supposed c-RX operation.
        self.cu3(theta, pi / 2, 3 * pi / 2, ctrl, target)
        # For the moment, QISKit adds a phase to the U-gate, so we
        # need to correct this phase with a controlled Rzz.
        self.crzz(pi, ctrl, target)


def crx(self, theta: float, ctrl: QubitType, target: QubitType) -> CRxGate:
    self._check_qubit(ctrl)
    self._check_qubit(target)
    self._check_dups([ctrl, target])
    return self._attach(CRxGate(theta, ctrl, target, self))


QuantumCircuit.crx = crx
CompositeGate.crx = crx
