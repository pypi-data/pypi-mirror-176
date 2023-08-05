from pymgrid.MicrogridGenerator import MicrogridGenerator
from pymgrid.microgrid.modular_microgrid.modular_microgrid import Microgrid
from pymgrid.microgrid.modules import *
from pymgrid.microgrid.envs import DiscreteMicrogridEnv

import numpy as np

import yaml

mgen = MicrogridGenerator(nb_microgrid=25)
mgen.generate_microgrid()
microgrid = mgen.microgrids[2]

modular_microgrid = Microgrid.from_nonmodular(microgrid)

env = DiscreteMicrogridEnv(modular_microgrid)

env.step(env.action_space.sample())

print(env.battery.item().dump())

print(env.genset.item().dump())

loaded_battery = yaml.safe_load(env.battery.item().dump())

print(loaded_battery == env.battery.item())

loaded_genset = yaml.safe_load(env.genset.item().dump())
print(loaded_genset == env.genset.item())

Microgrid.from_nonmodular(modular_microgrid.to_nonmodular()).to_nonmodular()
print(modular_microgrid)