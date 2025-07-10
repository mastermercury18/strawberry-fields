import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *
import tensorflow as tf

# initialize engine and program objects
eng = sf.Engine(backend="tf", backend_options={"cutoff_dim": 7})
circuit = sf.Program(1)

tf_alpha = tf.Variable(0.1)
tf_phi = tf.Variable(0.1)

alpha, phi = circuit.params("alpha", "phi")

with circuit.context as q:
    Dgate(alpha, phi) | q[0]

opt = tf.keras.optimizers.Adam(learning_rate=0.1)
steps = 50

for step in range(steps):

    # reset the engine if it has already been executed
    if eng.run_progs:
        eng.reset()

    with tf.GradientTape() as tape:
        # execute the engine
        results = eng.run(circuit, args={"alpha": tf_alpha, "phi": tf_phi})
        # get the probability of fock state |1>
        prob = results.state.fock_prob([1])
        # negative sign to maximize prob
        loss = -prob

    gradients = tape.gradient(loss, [tf_alpha, tf_phi])
    opt.apply_gradients(zip(gradients, [tf_alpha, tf_phi]))
    print("Probability at step {}: {}".format(step, prob))

def loss():
    # reset the engine if it has already been executed
    if eng.run_progs:
        eng.reset()

    # execute the engine
    results = eng.run(circuit, args={"alpha": tf_alpha, "phi": tf_phi})
    # get the probability of fock state |1>
    prob = results.state.fock_prob([1])
    # negative sign to maximize prob
    return -prob


tf_alpha = tf.Variable(0.1)
tf_phi = tf.Variable(0.1)


for step in range(steps):
    # In eager mode, calling Optimizer.minimize performs a single optimization step,
    # and automatically updates the parameter values.
    _ = opt.minimize(loss, [tf_alpha, tf_phi])
    parameter_vals = [tf_alpha.numpy(), tf_phi.numpy()]
    print("Parameter values at step {}: {}".format(step, parameter_vals))