
"""This module define some useful functions and types to deal with endianness.
"""

import typing
import qiskit

from .registers import QRegisterBase, CRegisterBase

# Type alias definition
GateContainer = typing.Union[qiskit.QuantumCircuit, qiskit.CompositeGate]

class QRegisterLE(QRegisterBase):
    """Quantum Register Little Endian."""
    pass

class QRegisterBE(QRegisterBase):
    """Quantum Register Big Endian."""
    pass

class QRegisterPhaseLE(QRegisterBase):
    """Quantum Register Little Endian in Quantum Fourier Transform state."""
    pass

class QRegisterPhaseBE(QRegisterBase):
    """Quantum Register Big Endian in Quantum Fourier Transform state."""
    pass


class CRegister(CRegisterBase):
    """Classical Register."""
    pass


def apply_LE_operation(container: GateContainer,
                       little_endian_operation,
                       qreg: qiskit.QuantumRegister):
    """Apply a little endian operation to a quantum register.
    This function will change the endianness of the given register if
    it is not already in little endian, apply the operation, and recover
    the initial endianness.
    Warning: if the type of the given register does not give any
             information on its endianness (inheriting from
             QRegisterLE or QRegisterBE) then the operation will be
             applied on the register without any endianness
             consideration.
    """

    if isinstance(qreg, QRegisterBE):
        qreg._reverse_access_endian()

    # Here we may have an instance of QRegisterBE which is
    # in little endian when we access it. This should be
    # avoided, that is why the method _reverse_access_endian
    # is "private".

    little_endian_operation(container, qreg)

    # As written above, we may have a strange register (labeled
    # as big endian but effectively in little endian). Don't
    # forget to fix this register by changing again it's
    # endianness.

    if isinstance(qreg, QRegisterBE):
        qreg._reverse_access_endian()

def apply_BE_operation(container: GateContainer,
                       big_endian_operation,
                       qreg: qiskit.QuantumRegister):
    """Apply a big endian operation to a quantum register.
    This function will change the endianness of the given register if
    it is not already in big endian, apply the operation, and recover
    the initial endianness.
    Warning: if the type of the given register does not give any
             information on its endianness (inheriting from
             QRegisterLE or QRegisterBE) then the operation will be
             applied on the register without any endianness
             consideration.
    """

    if isinstance(qreg, QRegisterLE):
        qreg._reverse_access_endian()

    # Here we may have an instance of QRegisterLE which is
    # in big endian when we access it. This should be
    # avoided, that is why the method _reverse_access_endian
    # is "private".

    big_endian_operation(container, qreg)

    # As written above, we may have a strange register (labeled
    # as little endian but effectively in big endian). Don't
    # forget to fix this register by changing again it's
    # endianness.

    if isinstance(qreg, QRegisterLE):
        qreg._reverse_access_endian()


def swap_endianness(self: GateContainer,
                    qreg: typing.Union[QRegisterBE, QRegisterLE]):
    """Swaps the endianness of qreg."""
    qubit_number = len(qreg)
    for i in range(qubit_number//2):
        self.swap(qreg[i], qreg[qubit_number-1-i])


