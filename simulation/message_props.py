from node_props import *
from block_props import *

message_types = ["proposal", "solution"]
class block_id_generator:
	def __init__(self):
		self.current_id = 1
		self.id_to_node = {}

	def new_id(self):
		pass

class message:
	def __init__(self, block, message_type, orig_author, final_author=None):
		if not isinstance(block, free_block):
			raise TypeError("block should be of type free_block; currently of type "+str(type(block))+".")
		self.block = block

		if message_type not in message_types:
			raise ValueError("message_type must be 'proposal' or 'solution'.")
		self.message_type = message_type

		if not isinstance(orig_author, cooperative_node):
			raise TypeError("orig_author should be of type cooperative_node; currently of type "+str(type(orig_author))+".")

		if message_type == "proposal":
			if final_author != None:
				raise ValueError("If message_type is 'proposal', final_author should be None.")
		else:
			if not isinstance(final_author, cooperative_node):
				raise TypeError("final_author should be of type cooperative_node; currently of type "+str(type(final_author))+".")
		self.final_author = final_author

	def __eq__(self, other):
		if not isinstance(other, message):
			raise TypeError("other must be of type message; currently of type "+str(type(other))+".")
		return self.block == other.block and self.message_type == other.message_type and self.orig_author == other.orig_author

class cooperative_node(person_node):
	def __init__(self, name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
		super().__init__(name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob)
		self.open_problems = set()
		self.closed_problems = {null_block: fixed_block(null_block)}

	def find_prob_message_by_author(self, orig_author):
		for x in self.open_problems:
			if x.orig_author == orig_author:
				return x
		raise KeyError("unrecognized orig_author")

	def create_problem_proposal(self):
		pass

	def add_fixed_block(self, free_seed):
		self.closed_problems[free_seed] = fixed_block(free_seed, self.closed_problems[free_seed.parent])

	def pass_message(self, message_instance, other):
		if not isinstance(message_instance, message):
			raise TypeError("message_instance should be of type message; currently of type "+str(type(message_instance))+".")

		if message_instance.message_type == "proposal":
			if message_instance.orig_author == self:
				pass
			elif message_instance.orig_author in [x.orig_author for x in other.open_problems]:
				pass
			else:
				other.open_problems.add(message_instance)
				for neigh in other.neighbors:
					if neigh != self:
						other.pass_message(message_instance, neigh)

		if message_instance.message_type == "solution":
			if message_instance.orig_author in [x.orig_author for x in other.open_problems]:
				other.open_problems.remove(other.find_prob_message_by_author(message_instance.orig_author))
			temp_list = list(other.closed_problems.keys())
			if message_instance.block not in temp_list:
				if message_instance.block.parent in temp_list:
					other.add_fixed_block(message_instance.block)
					for neigh in other.neighbors:
						if neigh != self:
							other.pass_message(message_instance, neigh)

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
		self.node_to_number = dict((self.name_to_node[item], j) for j, item in enumerate(self.node_names))

		if not isinstance(percentage_update_action, float):
			raise TypeError("percentage_update_action should be of type float; currently of type "+str(type(percentage_update_action))+".")
		self.percentage_update = percentage_update_action

	def run_update(self):
		to_update = sample(self.universe, int(np.floor(self.percentage_update*len(self.universe))))
		for node in to_update:
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
