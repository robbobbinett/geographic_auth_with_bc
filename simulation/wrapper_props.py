from random import choice, sample
from scipy.stats import bernoulli
from scipy.sparse import csc_matrix
import numpy as np
from node_props import *

class universe_wrapper:
	"""
	A wrapper which manages all the person_node instances to be used in a
	simulation. It handles all the person_node updates as a single event,
	and it outputs the adjacency matrix of the person_node neighborhood
	by a single method call.
	"""
	def __init__(self, universe, percentage_update_action=1.0):
		if not isinstance(universe, set):
			raise TypeError("universe should be of type set; currently of type "+str(type(universe))+".")
		if not all(isinstance(item, person_node) for item in universe):
			raise TypeError("All items in universe should be of type person_node. Currently, universe contains instances of the following types: "+", ".join(set([str(type(item)) for item in universe])))
		self.universe = universe

		self.node_names = [node.name for node in self.universe]
		self.node_names.sort()

		self.name_to_node = dict((node.name, node) for node in self.universe)
		self.node_to_number = dict((self.name_to_node[name], j) for j, name in enumerate(self.node_names))

		if not isinstance(percentage_update_action, float):
			raise TypeError("percentage_update_action should be of type float; currently of type "+str(type(percentage_update_action))+".")
		self.percentage_update = percentage_update_action

	def run_update(self):
		"""
		Calls person_node.update_action() for a fraction of the nodes of the universe.
		The fraction of nodes that is updated is percentage_update_action.
		The nodes are always updated in alphabetical order of their names.
		"""
		to_update = sample(self.universe, int(np.floor(self.percentage_update*len(self.universe))))
		for node_name in self.node_names:
			node = self.name_to_node[node_name]
			if node in to_update:
				node.update_action()

	def output_connections(self):
		connections_matrix = np.zeros((len(self.universe),)*2)
		for j, name in enumerate(self.node_names):
			for neigh in self.name_to_node[name].neighbors:
				connections_matrix[j, self.node_to_number[neigh]] = 1
		return csc_matrix(connections_matrix)

def make_universe_of_nodes(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
	universe = set()
	for j in range(num_nodes):
		universe.add(person_node("node_"+str(j), universe, add_behavior=add_behavior, drop_behavior=drop_behavior, pass_prob=pass_prob, get_add_prob=get_add_prob))
	return universe_wrapper(universe)
