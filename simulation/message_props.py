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
