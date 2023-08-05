from taurunner.main import *
from taurunner.body import Body
from taurunner.modules import make_initial_e
from taurunner.modules import make_initial_thetas
from taurunner.modules import make_propagator
import proposal as pp
import numpy as np

# set up MC
num_sim = 10000
en = 1e8
TR_specs = {
    'energy': en,
    'theta': 0.,
    'flavor': 16,
    'no_secondaries': False,
    'nevents': num_sim,
    'seed': 2,
    'xs_model': 'dipole',
    'no_losses': False
    }
rand = np.random.RandomState(TR_specs['seed'])
TR_specs['rand'] = rand
eini = make_initial_e(TR_specs, rand=rand)
thetas = make_initial_thetas(TR_specs, rand=rand)
body = Body(6.0, 5000.0)
tracks  = {theta:Chord(theta=theta, depth=0.) for theta in set(thetas)}
xs = CrossSections(TR_specs['xs_model'])
prop = make_propagator(body)

sim = run_MC(eini, thetas, body, xs, tracks, TR_specs, prop)

print(sim)
print("Shape: ")
print(sim.shape)
print("Interactions")
print(np.sum(sim['nNC']), np.sum(sim['nCC']))
print('Eout: {}'.format(np.sum(sim['Eout'])))
print('Ein : {}'.format(en*1e9*num_sim))
