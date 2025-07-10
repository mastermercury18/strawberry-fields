import strawberryfields as sf
from strawberryfields.ops import *
from numpy import pi, sqrt
import numpy as np

gaussian_cloning = sf.Program(4)

with gaussian_cloning.context as q:
    # state to be cloned
    alpha = 0.7+1.2j
    Coherent(np.abs(alpha), np.angle(alpha)) | q[0]

    # 50-50 beamsplitter
    BS = BSgate(pi/4, 0)

    # symmetric Gaussian cloning scheme
    BS | (q[0], q[1])
    BS | (q[1], q[2])
    MeasureX | q[1]
    MeasureP | q[2]
    Xgate(q[1].par * sqrt(2)) | q[0]
    Zgate(q[2].par * sqrt(2)) | q[0]

    # after the final beamsplitter, modes q[0] and q[3]
    # will contain identical approximate clones of the
    # initial state Coherent(0.1+0j)
    BS | (q[0], q[3])

eng = sf.Engine(backend="gaussian")
results = eng.run(gaussian_cloning, modes=[0, 3])

fidelity = sqrt(results.state.fidelity_coherent([0.7+1.2j, 0.7+1.2j]))
print(fidelity)

alpha = results.state.displacement()
print(alpha[0] - alpha[1] <= 1e-15)

# run the engine over an ensemble
reps = 1000
f = np.empty([reps])
a = np.empty([reps], dtype=np.complex128)

for i in range(reps):
    eng.reset()
    results = eng.run(gaussian_cloning, modes=[0])
    f[i] = results.state.fidelity_coherent([0.7+1.2j])
    a[i] = results.state.displacement()

print("Fidelity of cloned state:", np.mean(f))
print("Mean displacement of cloned state:", np.mean(a))
print("Mean covariance matrix of cloned state:", np.cov([a.real, a.imag]))

import seaborn as sns
sns.set(style="ticks")
sns.jointplot(a.real, a.imag, color="#4CB391")

