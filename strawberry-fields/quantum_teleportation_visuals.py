import strawberryfields as sf
from strawberryfields.ops import *

import numpy as np
from numpy import pi, sqrt

prog = sf.Program(3)

alpha = 1+0.5j
r = np.abs(alpha)
phi = np.angle(alpha)

with prog.context as q:
    # prepare initial states
    Coherent(r, phi) | q[0]
    Squeezed(-2) | q[1]
    Squeezed(2) | q[2]

    # apply gates
    BS = BSgate(pi/4, pi)
    BS | (q[1], q[2])
    BS | (q[0], q[1])

    # Perform homodyne measurements
    MeasureX | q[0]
    MeasureP | q[1]

    # Displacement gates conditioned on
    # the measurements
    Xgate(sqrt(2) * q[0].par) | q[2]
    Zgate(sqrt(2) * q[1].par) | q[2]

eng = sf.Engine('fock', backend_options={'cutoff_dim': 15})
result = eng.run(prog, shots=1, modes=None, compile_options={})
state = result.state

#reduced density matrix for mode q[2]
rho2 = np.einsum('kkllij->ij', state.dm())

#diagonal values of rho2 contain marginal fock state probabilities 
probs = np.real_if_close(np.diagonal(rho2))

from matplotlib import pyplot as plt
plt.bar(range(7), probs[:7])
plt.xlabel('Fock state')
plt.ylabel('Marginal probability')
plt.title('Mode 2')
plt.show()
