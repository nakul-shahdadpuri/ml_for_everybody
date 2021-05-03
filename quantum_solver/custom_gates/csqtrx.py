
"""This module contains functions to apply a controlled-sqrt(X) gate.
"""
from typing import Tuple
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
import hhl4x4.custom_gates.comment

QubitType = Tuple[QuantumRegister, int]


class CsqrtX(CompositeGate):

    def __init__(self, ctrl: QubitType, target: QubitType,
                 circuit: QuantumCircuit = None):
        """Initialize the CsqrtX class.

        :param ctrl: The control qubit used to control the sqrt(X) gate.
        :param target: The qubit on which the sqrt(X) gate is applied.
        :param circuit: The associated quantum circuit.
        """
        used_qubits = [ctrl, target]

        super().__init__(self.__class__.__name__,  # name
                         [],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit
        self.comment("c-sqrt(X)")
        self.cx(ctrl, target)
        self.cz(ctrl, target)
        self.h(target)
        self.t(target)
        self.tdg(ctrl)
        self.cx(ctrl, target)
        self.tdg(target)
        self.h(target)


def csqrtx(self, ctrl: QubitType, target: QubitType) -> CsqrtX:
    self._check_qubit(ctrl)
    self._check_qubit(target)
    self._check_dups([ctrl, target])
    return self._attach(CsqrtX(ctrl, target, self))


QuantumCircuit.csqrtx = csqrtx
CompositeGate.csqrtx = csqrtx
