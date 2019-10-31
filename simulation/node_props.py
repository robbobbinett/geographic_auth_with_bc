from random import choice, sample
from scipy.stats import bernoulli
from scipy.sparse import csc_matrix
import numpy as np

def default_drop(self):
	"""
	The default drop method to be used by the person_node class, given
	no other method is given. The idea is to drop a neighbor at random.
	"""
	to_drop = choice(self.neighbors)
	self.remove(to_drop)
	to_drop.remove(self)

def default_add(self):
	"""
	The default add method to be used by the person_node class, given
	no other method is given. The idea is, if the node has no neighbors,
	to add a random node from the universe of nodes that is not self; if
	the node does have neighbors, it attempts to add a random non-self
	node with probability 0.2 and attempts to add a neighbor's neighbor
	(that is not currently neighbor) with probability 0.8.
	"""
	if len(self.neighbors) == 0:
		cond = False
		while not cond:
			to_add = choice(self.universe)
			if len(to_add.neighbors) < 5 and to_add != self:
				cond = True
	else:
		cond = False
		while not cond:
			e = bernoulli.rvs(0.8, size=1)
			if e:
				recommender = choice(self.neighbors)
				to_add = choice(recommender.neighbors)
				if to_add not in self.neighbors:
					cond = True
			else:
				to_add = choice(self.universe)
				if len(to_add.neighbors) < 5 and to_add != self:
					cond = True
	self.neighbors.add(to_add)
	to_add.neighbors.add(self)

def default_get_add_prob(self):
	"""
	The default add_prob method of the person_node class, if no other
	method is passed in. The idea is, if the node chooses to not pass,
	it has 1.0 - 0.2x probability of adding a neighbor (where x is the
	number of neighbors it currently has) and the conjugate probability
	of dropping a neighbor.
	"""
	return 1.0 - 0.2*len(self.neighbors)

class person_node:
	"""
	This is the primitive to be used for simulating locality of persons.

	Transactions will only occur between adjacent person_nodes, and
	transactions and blocks will only be propagated between adjacent
	person_nodes.

	person_node A has person_node B as a neighbor iff B has A as a neighbor.
	On each person_timestep (which might be distinct from a machine_timestep),
	a person_node maintains its set of neighbors with probability pass_prob
	and otherwise adds or drops neighbors according to the output of
	self.get_add_prob.
	"""
	def __init__(self, name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
		if not isinstance(name, str):
			raise TypeError("name must be of type str; currently of type "+str(type(name))+".")
		self.name = name

		if not isinstance(universe, set):
			raise TypeError("universe must be of type set; currently of type "+str(type(universe))+".")
		self.universe = universe

		self.neighbors = set()

		if not isinstance(pass_prob, float):
			raise TypeError("pass_prob must be of type float; currently of type "+str(type(pass_prob))+".")
		self.pass_prob=pass_prob

		setattr(self, "add", add_behavior)
		setattr(self, "drop", drop_behavior)
		setattr(self, "add_prob", get_add_prob)

	def update_action(self):
		"""
		Do nothing with probability self.pass_prob. Otherwise, call
		self.get_add_prob to determine whether a neighbor is added or
		dropped.
		"""
		passive = bernoulli.rvs(self.pass_prob, size=1)
		if not passive:
			prob_add = self.get_add_prob()
			adding = bernoulli(prob_add, size=1)
			if adding:
				self.add()
			else:
				self.drop()

	def __str__(self):
		return self.name

	def __hash__(self):
		"""
		Have the hash of self be equal to the hash of self.name; this is so
		we can use this class as keys for dictionaries, sets, etc. without
		having to explicitly typecast to str.
		"""
		return hash(self.name)

	def __eq__(self, other):
		"""
		Equality can only hold between two instances of type person_node.
		Equality holds, given the above, iff self.name == other.name.

		For our purposes, it is sufficient to make sure that we use each
		node name exactly once to make this equality method valid.
		"""
		if not isinstance(other, person_node):
			raise TypeError("other must be of type person_node; currently of type "+str(type(other))+".")
		return self.name == other.name

class universe_wrapper:
	"""
	A wrapper which manages all the person_node instances to be used in a
	simulation. It handles all the person_node updates as a single event,
	and it outputs the adjacency matrix of the person_node neighborhood
	by a single method call.
	"""
	def __init__(self, universe, percentage_update_action=0.1):
		if not isinstance(universe, set):
			raise TypeError("universe should be of type set; currently of type "+str(type(universe))+".")
		if not all(isinstance(item, person_node) for item in universe):
			raise TypeError("All items in universe should be of type person_node. Currently, universe contains instances of the following types: "+", ".join(set([str(type(item)) for item in universe])))
		self.universe = universe

		self.node_names = [str(node) for node in self.universe]
		self.node_names.sort()

		self.name_to_node = dict((str(node), node) for node in self.universe)
		self.node_to_number = dict((item, j) for j, item in enumerate(self.node_names))

		if not isinstance(percentage_update_action, float):
			raise TypeError("percentage_update_action should be of type float; currently of type "+str(type(percentage_update_action))+".")
		self.percentage_update = percentage_update_action

	def run_update(self):
		to_update = sample(self.universe, np.floor(self.percentage_update*len(self.universe)))
		for node in to_update:
			node.update_action()

	def output_connections(self):
		connections_matrix = np.zeros((len(self.universe),)*2)
		for j, name in enumerate(self.node_names):
			for neigh in self.name_to_node[name].neighbors:
				connections_matrix[j, self.name_to_number[neigh]] = 1
		return csc_matrix(connections_matrix)

def make_universe_of_nodes(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
	universe = set()
	for j in range(num_nodes):
		universe.add(person_node("node_"+str(j), universe, add_behavior=add_behavior, drop_behavior=drop_behavior, pass_prob=pass_prob, get_add_prob=get_add_prob))
	return universe_wrapper(universe)
