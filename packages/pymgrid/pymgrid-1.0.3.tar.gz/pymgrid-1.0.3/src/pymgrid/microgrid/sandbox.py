from pymgrid.MicrogridGenerator import MicrogridGenerator
from pymgrid.microgrid.modular_microgrid.modular_microgrid import Microgrid


mgen = MicrogridGenerator(nb_microgrid=25)
mgen.generate_microgrid()
microgrid = mgen.microgrids[0]

modular_microgrid = Microgrid.from_nonmodular(microgrid)
print(modular_microgrid)
