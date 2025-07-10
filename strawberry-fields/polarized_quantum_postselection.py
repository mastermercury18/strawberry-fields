# Import and preliminaries
import strawberryfields as sf
from strawberryfields.ops import Ket, BSgate, Interferometer
import numpy as np

cutoff_dim = 5  # (1+ total number of photons)
paths = 4
modes = 2 * paths

initial_state = np.zeros([cutoff_dim] * modes, dtype=np.complex)
# The ket below corresponds to a single horizontal photon in each of the modes
initial_state[1, 0, 1, 0, 1, 0, 1, 0] = 1
# Permutation matrix
X = np.array([[0, 1], [1, 0]])

# Here is the main program
# We create the input state and then send it through a network of beamsplitters and swaps.
prog = sf.Program(8)
with prog.context as q:
    Ket(initial_state) | q  # Initial state preparation
    for i in range(paths):
        BSgate() | (q[2 * i], q[2 * i + 1])  # First layer of beamsplitters
    Interferometer(X) | (q[1], q[3])
    Interferometer(X) | (q[5], q[7])
    BSgate() | (q[2], q[3])
    BSgate() | (q[4], q[5])
    Interferometer(X) | (q[3], q[5])
    BSgate().H | (q[2], q[3])
    BSgate().H | (q[4], q[5])

# We run the simulation
eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff_dim})
result = eng.run(prog)
state = result.state
ket = state.ket()

# Check the normalization of the ket.
# This does give the exact answer because of the cutoff we chose.
print("The norm of the ket is ", np.linalg.norm(ket))

sub_ket1 = np.round(ket[:, :, 1, 0, 1, 0, :, :], 14)  # postselect on correct pattern
p1 = np.round(np.linalg.norm(sub_ket1) ** 2, 14)  # Check the probability of this event
print("The probability is ", p1)
print("The expected probability is ", 1 / 32)

# These are the only nonzero components
ind1 = np.array(np.nonzero(np.real_if_close(sub_ket1))).T
print("The indices of the nonzero components are \n ", ind1)

# And these are their coefficients
print("The nonzero components have values ", [sub_ket1[tuple(ind)] for ind in ind1])

# Transpose the ket
ket_t = ket.transpose(2, 3, 4, 5, 0, 1, 6, 7)
# Postselection patterns:
patterns = [
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
]

sub_kets = [np.round(ket_t[tuple(ind)], 15) for ind in patterns]
ps = np.array(list(map(np.linalg.norm, sub_kets))) ** 2
indices = np.array([np.array(np.nonzero(sub_ket)).T for sub_ket in sub_kets])
print(
    "The indices of the nonzero components for the six different postselections are \n",
    indices,
)

# The successful postselection events occur with the same probability
print("The success probabilities for each pattern are the same \n", ps)
