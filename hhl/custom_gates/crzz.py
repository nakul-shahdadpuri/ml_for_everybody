
from typing import Tuple
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
import hhl4x4.custom_gates.comment

QubitType = Tuple[QuantumRegister, int]


class CRZZGate(CompositeGate):

    def __init__(self, theta: float, ctrl: QubitType, target: QubitType,
                 circuit: QuantumCircuit = None):
        """Initialize the CRzzGate class.

        :param theta: Phase added to the quantum state of qubit.
        :param ctrl: The control qubit used to control the RZZ gate.
        :param target: The qubit on which the RZZ gate is applied.
        :param circuit: The associated quantum circuit.
        """
        used_qubits = [ctrl, target]

        super().__init__(self.__class__.__name__,  # name
                         [theta],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit

        self.comment("c-RZZ")
        self.cu1(theta, ctrl, target)
        self.cx(ctrl, target)
        self.cu1(theta, ctrl, target)
        self.cx(ctrl, target)


def crzz(self, theta: float, ctrl: QubitType, target: QubitType) -> CRZZGate:
    self._check_qubit(ctrl)
    self._check_qubit(target)
    self._check_dups([ctrl, target])
    return self._attach(CRZZGate(theta, ctrl, target, self))


QuantumCircuit.crzz = crzz
CompositeGate.crzz = crzz
