import math
from node_props import *

def _nop(self):
	"""
	No-operation.
	Used here as a placeholder for the required arguments for the person_node constructor.
	"""
	pass

def toroidal_distance(x1, y1, x2, y2):
	"""
	Computes the distance of the point (x1, y1) to the point (x2, y2)
	assuming that these points are in the unit torus [0, 1) x [0, 1).
	"""
	return min([math.hypot(x1 - x2 + xdelta, y1 - y2 + ydelta)
		for xdelta in [-1, 0, 1]
		for ydelta in [-1, 0, 1]])


class toroidal_node(person_node):
	"""
	Toroidal node.
	Each node is a vector in the unit torus [0, 1) x [0, 1).

	Constructor arguments:
	- name: Name of the node
	- universe: (Shared) list of nodes that this node belongs to
	- r: Radius of connectivity.
		Two nodes will be adjacent if they are within distance r of each other.
	- s: Movement at each step.
		This is the number of units the node will move at each call to update_action.
	- rng: Random number generator.
		Must be a parameter-less function that returns a number in [0, 1)
		chosen uniformly at random.
	"""

	def __init__(self, name, universe, r, s, rng):
		super().__init__(name, universe, add_behavior=_nop, drop_behavior=_nop, pass_prob=1.0, get_add_prob=lambda x: 1.0)
		self.r = r
		self.s = s
		self.x = rng()
		self.y = rng()

	def distance_to(self, other):
		"""
		Computes the distance between this node and the given target node.
		"""
		return toroidal_distance(self.x, self.y, other.x, other.y)

	def move(self):
		"""
		Moves the node a single simulation step.
		"""
		theta = rng() * 2 * math.pi
		self.x += s * math.cos(theta)
		self.y += s * math.sin(theta)

	def update_neighbors(self):
		"""
		Sets self.neighbors to be all nodes of self.universe
		that are within a distance of self.r of self.
		"""
		# Clear the list
		for neighbor in self.neighbors:
			neighbor.neighbors.remove(self)
		self.neighbors.clear()

		# Compute the new neighbors
		for neighbor_candidate in self.universe:
			if self.distance_to(neighbor_candidate) < self.r:
				self.neighbors.add(neighbor_candidate)
				neighbor_candidate.neighbors.add(self)

	def update_action(self):
		"""
		Moves and updates neighbors.
		Overrides person_node.update_action.
		"""
		self.move()
		self.update_neighbors()
