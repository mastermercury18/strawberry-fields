import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *

prog = sf.Program(3)

with prog.context as q:
    # State preparation in Blackbird
    Fock(1) | q[0]
    Coherent(0.5, 2) | q[1]

with prog.context as q:
    S = Squeezed(1)
    S | q[0]
    S | q[1]

with prog.context as q:
    # Apply the Displacement gate to qumode 0
    alpha = 2.0 + 1j
    Dgate(np.abs(alpha), np.angle(alpha)) | q[0]

    # Apply the Rotation gate
    phi = 3.14 / 2
    Rgate(phi) | q[0]

    # Apply the Squeezing gate
    Sgate(2.0, 0.17) | q[0]

    # Apply the Beamsplitter gate to qumodes 0 & 1
    BSgate(3.14 / 10, 0.223) | (q[0], q[1])

    # Apply the Cubic Phase gate (VGate) to qumode 0
    gamma = 0.1
    Vgate(gamma) | q[0]

with prog.context as q:
      V = Vgate(gamma)
      V.H | q[0]

with prog.context as q:
    # Homodyne measurement at angle phi
    phi = 0.25 * 3.14
    MeasureHomodyne(phi) | q[0]

    # Special homodyne measurements
    MeasureX | q[0]
    MeasureP | q[1]

    # Heterodyne measurement
    MeasureHeterodyne() | q[0]
    MeasureHD           | q[1]  # shorthand

    # Number state measurements of various qumodes
    MeasureFock() | q[0]
    MeasureFock() | (q[1], q[2]) # multiple modes

    