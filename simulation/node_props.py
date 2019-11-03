from random import choice, sample
from scipy.stats import bernoulli
from scipy.sparse import csc_matrix
import numpy as np

def default_drop(self):
	"""
	The default drop method to be used by the person_node class, given
	no other method is given. The idea is to drop a neighbor at random.
	"""
	to_drop = choice(list(self.neighbors))
	self.neighbors.remove(to_drop)
	to_drop.neighbors.remove(self)

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
			to_add = choice(list(self.universe))
			if len(to_add.neighbors) < 5 and to_add != self:
				cond = True
	else:
		cond = False
		while not cond:
			e = bernoulli.rvs(0.8, size=1)
			if e:
				recommender = choice(list(self.neighbors))
				to_add = choice(list(recommender.neighbors))
			else:
				to_add = choice(list(self.universe))
			if len(to_add.neighbors) < 5 and to_add != self and (to_add not in self.neighbors):
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

		setattr(self, "add", lambda: add_behavior(self))
		setattr(self, "drop", lambda: drop_behavior(self))
		setattr(self, "add_prob", lambda: get_add_prob(self))


	def update_action(self):
		"""
		Do nothing with probability self.pass_prob. Otherwise, call
		self.get_add_prob to determine whether a neighbor is added or
		dropped.
		"""
		passive = bernoulli.rvs(self.pass_prob, size=1)
		if not passive:
			prob_add = self.add_prob()
			try:
				adding = bernoulli.rvs(prob_add, size=1)
			except ValueError:
				raise ValueError("The value of prob_add is "+str(prob_add))
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
