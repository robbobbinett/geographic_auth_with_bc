from random import choice, sample
from scipy.stats import bernoulli
import numpy as np

def default_drop(self):
	to_drop = choice(self.neighbors)
	self.remove(to_drop)
	to_drop.remove(self)

def default_add(self):
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
	return 1.0 - 0.2*len(self.neighbors)

class person_node:
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
		return hash(self.name)

	def __eq__(self, other):
		if not isinstance(other, person_node):
			raise TypeError("other must be of type person_node; currently of type "+str(type(other))+".")
		return self.name == other.name

class universe_wrapper:
	def __init__(self, universe, percentage_update_action=0.1):
		if not isinstance(universe, set):
			raise TypeError("universe should be of type set; currently of type "+str(type(universe))+".")
		if not all(isinstance(item, person_node) for item in universe):
			raise TypeError("All items in universe should be of type person_node. Currently, universe contains instances of the following types: "+", ".join(set([str(type(item)) for item in universe])))
		self.universe = universe

		if not isinstance(percentage_update_action, float):
			raise TypeError("percentage_update_action should be of type float; currently of type "+str(type(percentage_update_action))+".")
		self.percentage_update = percentage_update_action

	def run_update(self):
		to_update = sample(self.universe, np.floor(self.percentage_update*len(self.universe)))
		for node in to_update:
			node.update_action()

def make_universe_of_nodes(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
	universe = set()
	for j in range(num_nodes):
		universe.add(person_node("node_"+str(j), universe, add_behavior=add_behavior, drop_behavior=drop_behavior, pass_prob=pass_prob, get_add_prob=get_add_prob))
	return universe_wrapper(universe)
