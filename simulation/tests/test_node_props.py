import simpy
from tqdm import tqdm
from node_props import make_universe_of_nodes

env = simpy.Environment()

def test_universe_wrapper_doesnt_crash():
	"""
	Run all methods of the universe_wrapper class (which in turn
	runs all methods of the person_node class). The size of the
	universe should hopefully preclude (in probability) errors
	arising
	"""
	universe = make_universe_of_nodes(1000)

	# Running 1000 updates per node on each node in a 1000-node universe
	for _ in tqdm(range(1000)):
		universe.run_update()

	test_mat = universe.output_connections()
