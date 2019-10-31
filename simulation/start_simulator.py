import simpy
from tqdm import tqdm
from node_props import make_universe_of_nodes

env = simpy.Environment()
universe = make_universe_of_nodes(1000)

for _ in tqdm(range(100)):
	universe.run_update()
