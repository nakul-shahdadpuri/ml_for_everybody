
"""Implementation of a comment instruction.

The comment instruction is a hack to be able to insert comments in the
generated OpenQASM code. Comments are then ignored and removed by the
Qiskit compiler so they will only appear in the generated OpenQASM.

The Comment gate overloads the Barrier gate, which *does not* change the
circuit result but *might change* the final OpenQASM code by preventing
some optimisations.
"""

import qiskit
from qiskit.extensions.standard.barrier import Barrier


class Comment(Barrier):
    """Instruction inserting a comment in the OpenQASM code."""

    def __init__(self, text: str, qubits, circ):
        """Create new comment."""
        super().__init__(qubits, circ)
        self._text = text

    def inverse(self):
        """Do nothing. Return self."""
        return self

    def qasm(self):
        """Return OpenQASM string."""
        return "// {}".format(self._text)

    def reapply(self, circ):
        """Reapply this comment."""
        self._modifiers(circ.comment(self._text))

    def q_if(self, *qregs):
        self._text = ("c-" * len(qregs)) + self._text
        return self


def comment(self, text: str):
    """Write a comment to circuit."""
    all_qubits = []
    circuit = self
    while not hasattr(circuit, 'regs'):
        circuit = circuit.circuit
    for _, register in circuit.regs.items():
        if isinstance(register, qiskit.QuantumRegister):
           all_qubits.extend((register[i] for i in range(len(register))))
    return self._attach(Comment(text, all_qubits, self))


qiskit.QuantumCircuit.comment = comment
qiskit.CompositeGate.comment = comment
