# Usual imports
import strawberryfields as sf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm

# Simulation and cat state parameters
nmodes = 1
cutoff = 30
q = 4.0
p = 0.0
hbar = 2
alpha = (q + 1j * p) / np.sqrt(2 * hbar)
k = 1

# SF program
prog_cat_fock = sf.Program(nmodes)
with prog_cat_fock.context as q:
    sf.ops.Catstate(a=np.absolute(alpha), phi=np.angle(alpha), p=k) | q

eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff, "hbar": hbar})
state = eng.run(prog_cat_fock).state

# We now plot it
xvec = np.linspace(-15, 15, 401)
W = state.wigner(mode=0, xvec=xvec, pvec=xvec)
Wp = np.round(W.real, 4)
scale = np.max(Wp.real)
nrm = mpl.colors.Normalize(-scale, scale)
plt.axes().set_aspect("equal")
plt.contourf(xvec, xvec, Wp, 60, cmap=cm.RdBu, norm=nrm)
plt.show()

prog_cat_bosonic = sf.Program(nmodes)

with prog_cat_bosonic.context as q:
    sf.ops.Catstate(a=np.absolute(alpha), phi=np.angle(alpha), p=k) | q

eng = sf.Engine("bosonic", backend_options={"hbar": hbar})
state = eng.run(prog_cat_bosonic).state

means = state.means()
print(means)

covs = state.covs()
print(covs)

weights = state.weights()
print(weights)

def gaussian_func_gen(mu, V):
    """Generates a function that when evaluated returns
    the value of a normalized Gaussian specified in terms
    of a vector of means and a covariance matrix.

    Args:
        mu (array): vector of means
        V (array): covariance matrix

    Returns:
        (callable): a normalized Gaussian function
    """
    Vi = np.linalg.inv(V)
    norm = 1.0 / np.sqrt(np.linalg.det(2 * np.pi * V))
    fun = lambda x: norm * np.exp(-0.5 * (x - mu) @ Vi @ (x - mu))
    return fun


def evaluate_fun(fun, xvec, yvec):
    """Evaluate a function a 2D in a grid of points.

    Args:
        fun (callable): function to evaluate
        xvec (array): values of the first variable of the function
        yvec (array): values of the second variable of the function

    Returns:
        (array): value of the function in the grid
    """
    return np.array([[fun(np.array([x, y])) for x in xvec] for y in xvec])


funs = [gaussian_func_gen(means[i], covs[i]) for i in range(len(means))]

Wps = [weights[i] * evaluate_fun(funs[i], xvec, xvec) for i in range(len(weights))]

print(np.allclose(sum(Wps).imag, 0))

print(np.allclose(Wps[2],  Wps[3].conj()))
print(np.allclose(Wps[0].imag, 0))
print(np.allclose(Wps[1].imag, 0))

fig, axs = plt.subplots(1, 4, figsize=(10, 2.2))
for i in range(4):
    Wp = np.round(Wps[i].real, 4)
    axs[i].contourf(xvec, xvec, Wp, 60, cmap=cm.RdBu, norm=nrm)
    if i != 0:
        axs[i].set_yticks([])
plt.show()

Wcat = sum(Wps)
plt.axes().set_aspect("equal")
plt.contourf(xvec, xvec, Wcat.real, 60, cmap=cm.RdBu, norm=nrm)
plt.show()