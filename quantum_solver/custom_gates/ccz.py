
"""This module contains functions to apply a doubly controlled Z gate.
"""
from typing import Tuple
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
import hhl4x4.custom_gates.comment

QubitType = Tuple[QuantumRegister, int]


class CCZGate(CompositeGate):

    def __init__(self, ctrl1: QubitType, ctrl2: QubitType, target: QubitType,
                 circuit: QuantumCircuit = None):
        """Initialize the CCZGate class.

        :param ctrl1: The first control qubit used to control the CCZ gate.
        :param ctrl2: The second control qubit used to control the CCZ gate.
        :param target: The qubit on which the Z gate is applied.
        :param circuit: The associated quantum circuit.
        """
        used_qubits = [ctrl1, ctrl2, target]

        super().__init__(self.__class__.__name__,  # name
                         [],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit

        self.comment("CCZ")
        from qiskit.extensions.standard.h import HGate
        self._attach(HGate(target, circuit).inverse())
        self.ccx(ctrl1, ctrl2, target)
        self._attach(HGate(target, circuit).inverse())


def ccz(self, ctrl1: QubitType, ctrl2: QubitType, target: QubitType) -> CCZGate:
    self._check_qubit(ctrl1)
    self._check_qubit(ctrl2)
    self._check_qubit(target)
    self._check_dups([ctrl1, ctrl2, target])
    return self._attach(CCZGate(ctrl1, ctrl2, target, self))


QuantumCircuit.ccz = ccz
CompositeGate.ccz = ccz
