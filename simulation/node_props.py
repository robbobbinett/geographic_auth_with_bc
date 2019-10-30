from random import choice
from scipy.stats import bernoulli

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
