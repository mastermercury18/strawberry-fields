import strawberryfields as sf
from strawberryfields.ops import *

import numpy as np
from numpy import pi, sqrt

# set the random seed
np.random.seed(42)

# initialize the program on three quantum registers 
prog = sf.Program(3)

#prepare the coherent state |alpha> (gaussian func centered at alpha = 1 + 0.5i) to teleport
alpha = 1+0.5j
r = np.abs(alpha)
phi = np.angle(alpha)

# encode alice and bob as squeezed states 

with prog.context as q:
    # prepare initial states
    Coherent(r, phi) | q[0]
    Squeezed(-2) | q[1]
    Squeezed(2) | q[2]

    # apply gates
    # analogous to CNOT gates in Qiskit 
    BS = BSgate(pi/4, pi)
    BS | (q[1], q[2])
    BS | (q[0], q[1])

    # Perform homodyne measurements on position and momentum 
    MeasureX | q[0]
    MeasureP | q[1]

    # Displacement gates conditioned on the measurements
    # analagous procedure in qiskit 
    Xgate(sqrt(2) * q[0].par) | q[2]
    Zgate(-sqrt(2) * q[1].par) | q[2]

# choose the fock backend to run the simulation 
eng = sf.Engine('fock', backend_options={"cutoff_dim": 15})
result = eng.run(prog, shots=1, modes=None, compile_options={})
samples = result.samples
print(samples)
state = result.state
print(state)

