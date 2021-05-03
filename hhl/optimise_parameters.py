import typing
import qiskit
import numpy as np
import scipy.linalg as la

import hhl4x4.custom_gates.hhl4x4

QubitType = typing.Tuple[qiskit.QuantumRegister, int]


def hamiltonian_error(power: int, display_digit: int):
    """Generate and return a function that will be given to the optimiser.

    The returned function will compute the error between the ideal unitary
    matrix (raised to the given power) and the simulated one with the set
    a parameters given by the optimizer.https://arxiv.org/abs/1110.2232v2

    :param power: the power we want to simulate.
    """

    def ret(params: typing.Sequence[float]) -> float:
        """Computes the error between the ideal matrix and the simulated one.

        :param params: parameters used in the quantum circuit.
        :return: the 2-norm distance between the ideal matrix and the simulated
        one.
        """
        list_format = ','.join(
            ["{: ." + str(display_digit) + "f}" for i in range(len(params))])
        print(("Computing U^{:<2} error with [" + list_format + "]: ").format(
            2 ** power, *params), end='')

        def swap(U):
            """Change the quantum gate representation.

            Qiskit uses a different endianness which change the unitary matrices
            representing quantum gates. This function takes a quantum gate "as
            we are used to represent them" and transform it "as Qiskit
            represents them".

            :param U: the matrix to change.
            :return: the adapted matrix.
            """
            from copy import deepcopy
            cpy = deepcopy(U)
            cpy[[1, 2], :] = cpy[[2, 1], :]
            cpy[:, [1, 2]] = cpy[:, [2, 1]]
            return cpy

        ancilla = qiskit.QuantumRegister(1)
        b = qiskit.QuantumRegister(2)
        classical = qiskit.ClassicalRegister(1)

        circuit = qiskit.QuantumCircuit(ancilla, b, classical)

        circuit.hamiltonian4x4(ancilla[0], b, params).inverse()

        unitary_sim = qiskit.Aer.get_backend('unitary_simulator')
        res = qiskit.execute([circuit], unitary_sim).result()
        unitary = res.get_unitary()

        A = .25 * np.array(
            [[15, 9, 5, -3], [9, 15, 3, -5], [5, 3, 15, -9], [-3, -5, -9, 15]])
        t0 = 2 * np.pi
        expA = swap(la.expm(-1.j * A * t0 * (2 ** power / 16)))
        unit = unitary[1::2, 1::2]
        np.set_printoptions(precision=2)
        err = la.norm(unit - expA)
        print("{: g}".format(err), end='\r', flush=True)
        return err

    return ret


def main():
    # Optimise!
    import scipy.optimize as opt
    import argparse

    parser = argparse.ArgumentParser(
        description='Find the optimum parameters for Hamiltonian simulation.')
    # parser.add_argument('--precision', default=1e-7, type=float,
    #                     help="Desired precision for the final Hamiltonian.")
    parser.add_argument("--maxiter", type=int, default=1000,
                        help="Maximum number of iterations (default to 1000).")
    parser.add_argument("--display-precision", type=int, default=8,
                        help="Number of digits needed when the parameters are "
                             "displayed (default to 8).")
    args = parser.parse_args()

    for power in range(4):
        opt_res = opt.minimize(hamiltonian_error(power, args.display_precision),
                               [0.2, 0.38, 0.98, 1.88, 0.59],
                               options={"maxiter": args.maxiter})
        print()


if __name__ == '__main__':
    main()
