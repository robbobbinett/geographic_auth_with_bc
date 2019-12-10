from toroidal_node import *
from message_props import *

class coop_tor_node(toroidal_node, cooperative_node):
	def __init__(self, name, universe, r, s, rng):
		toroidal_node.__init__(self, name, universe, r, s, rng)
		self.open_problems = {}
		self.closed_problems = {null_block: fixed_block(null_block)}
		self.problem_posed = False
		self.message_queue = []

def make_coop_tor_wrapper(num_nodes, r, s, rng):
	universe = set()
	for j in range(num_nodes):
		universe.add(coop_tor_node("node_"+str(j), universe, r, s, rng))
	return cooperative_wrapper(universe)
