from message_props import make_cooperative_wrapper

def full_clique_drop(self):
	"""
	Never drop a neighbor.
	"""
	pass

def full_clique_add(self):
	"""
	Add all nodes in universe as neighbors
	"""
	for node in self.universe:
		for other in self.universe:
			if node != other:
				node.neighbors.add(other)

def make_full_clique(num_nodes):
	"""
	Initialize universe as full clique
	"""
	chance_the = make_cooperative_wrapper(num_nodes)
	for node in chance_the.universe:
		for other_node in chance_the.universe:
			if node != other_node:
				node.neighbors.add(other_node)
	return chance_the
