import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *

prog = sf.Program(2)

import tensorflow as tf

# we can create symbolic parameters one by one
alpha = prog.params("alpha")

# or create multiple at the same time
theta_bs, phi_bs = prog.params("theta_bs", "phi_bs")

with prog.context as q:
    # States
    Coherent(alpha) | q[0]
    # Gates
    BSgate(theta_bs, phi_bs) | (q[0], q[1])
    # Measurements
    MeasureHomodyne(0.0) | q[0]

eng = sf.Engine(backend="tf", backend_options={"cutoff_dim": 7})

eng.run(prog)

mapping = {"alpha": tf.Variable(0.5), "theta_bs": tf.constant(0.4), "phi_bs": tf.constant(0.0)}

result = eng.run(prog, args=mapping)
print(result.samples)

state = result.state
print("Density matrix element [0,0,1,2]:", state.dm()[0, 0, 1, 2])

eng.reset()
prog = sf.Program(1)

alpha = prog.params("alpha")

with prog.context as q:
    Dgate(alpha) | q

# Assign our TensorFlow variables, so that we can
# refer to them later when differentiating/training.
a = tf.Variable(0.43)

with tf.GradientTape() as tape:
    # Here, we map our quantum free parameter `alpha`
    # to our TensorFlow variable `a` and pass it to the engine.

    result = eng.run(prog, args={"alpha": a})
    state = result.state

    # Note that all processing, including state-based post-processing,
    # must be done within the gradient tape context!
    mean, var = state.mean_photon(0)

# test that the gradient of the mean photon number is correct

grad = tape.gradient(mean, [a])
print("Gradient:", grad)

print("Exact gradient:", 2 * a)
print("Exact and TensorFlow gradient agree:", np.allclose(grad, 2 * a))