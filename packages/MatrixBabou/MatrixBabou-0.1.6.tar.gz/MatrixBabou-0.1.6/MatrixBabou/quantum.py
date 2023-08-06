import qiskit
from qiskit import Aer, transpile, assemble
from qiskit.circuit.library import QFT
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.quantum_info import state_fidelity
from qiskit.aqua.algorithms import HHL, NumPyLSsolver
from qiskit.aqua.components.eigs import EigsQPE
from qiskit.aqua.components.reciprocals import LookupRotation
from qiskit.aqua.operators import MatrixOperator
from qiskit.aqua.components.initial_states import Custom
import numpy as np

def create_eigs(matrix, num_auxiliary, num_time_slices, negative_evals):
    ne_qfts = [None, None]
    if negative_evals:
        num_auxiliary += 1
        ne_qfts = [QFT(num_auxiliary - 1), QFT(num_auxiliary - 1).inverse()]

    return EigsQPE(MatrixOperator(matrix=matrix),
                   QFT(num_auxiliary).inverse(),
                   num_time_slices=num_time_slices,
                   num_ancillae=num_auxiliary,
                   expansion_mode='suzuki',
                   expansion_order=2,
                   evo_time=np.pi*3/4,
                   negative_evals=negative_evals,
                   ne_qfts=ne_qfts)
                   
def fidelity(hhl, ref):
    solution_hhl_normed = hhl / np.linalg.norm(hhl)
    solution_ref_normed = ref / np.linalg.norm(ref)
    fidelity = state_fidelity(solution_hhl_normed, solution_ref_normed)
    return fidelity
    
def HHL_QUANTUM(A,b):
    ''' --> Note that dim(A) should be equal to 2^n   : it's preferable to chose dim(A)<2^3   . "that's need more time in quantum_Ibm !"
       ---> A : Hermitian Matrix .
       ---> b: vector with dim(b)=dim(A[:,1])
      ----> Result: Solution , probability , Fidelity.
    '''          
    
    orig_size = len(b)
    A,b, truncate_powerdim, truncate_hermitian = HHL.matrix_resize(A, b)

    # Initialize eigenvalue finding module
    eigs = create_eigs(A, len(A)+1, 50, False)
    num_q, num_a = eigs.get_register_sizes()

    # Initialize initial state module
    init_state = Custom(num_q, state_vector=b)

    # Initialize reciprocal rotation module
    reci = LookupRotation(negative_evals=eigs._negative_evals, evo_time=eigs._evo_time)

    algo = HHL(A,b, truncate_powerdim, truncate_hermitian, eigs,init_state, reci, num_q, num_a, orig_size)


    circ=algo.construct_circuit(measurement=True)
    result = algo.run(QuantumInstance(Aer.get_backend('statevector_simulator')))
    result_ref = NumPyLSsolver(A,b).run()

    fid=fidelity(result['solution'], result_ref['solution'])
    return np.round(result['solution'], 5),result['probability_result'],fid
from qiskit.algorithms.linear_solvers.hhl import HHL as hl1
def quantum_circuit(A,b):
    hhl_sol= hl1().solve(A,b)
    print(hhl_sol.state)


