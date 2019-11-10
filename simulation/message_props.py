from random import choice, sample
from node_props import *
from block_props import *

message_types = ["proposal", "solution"]
class block_id_generator:
	def __init__(self):
		self.current_id = 1
		self.id_to_node = {}

	def new_id(self):
		pass

num_highest_nodes_to_return = 10

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
		self.orig_author = orig_author

		if message_type == "proposal":
			if final_author != None:
				raise ValueError("If message_type is 'proposal', final_author should be None.")
		else:
			if not isinstance(final_author, cooperative_node):
				raise TypeError("final_author should be of type cooperative_node; currently of type "+str(type(final_author))+".")
		self.final_author = final_author

	def __hash__(self):
		return hash(self.block) + hash(self.message_type) + hash(self.orig_author)

	def __eq__(self, other):
		if not isinstance(other, message):
			raise TypeError("other must be of type message; currently of type "+str(type(other))+".")
		return self.block == other.block and self.message_type == other.message_type and self.orig_author == other.orig_author

class cooperative_node(person_node):
	def __init__(self, name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
		super().__init__(name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob)
		self.open_problems = set()
		self.closed_problems = {null_block: fixed_block(null_block)}
		self.problem_posed = False
		self.message_queue =[]

	def find_prob_message_by_author(self, orig_author):
		for x in self.open_problems:
			if x.orig_author == orig_author:
				return x
		raise KeyError("unrecognized orig_author")

	def add_fixed_block(self, message_instance):
		try:
			self.open_problems.remove(message_instance)
			free_seed = message_instance.block
			self.closed_problems[free_seed] = fixed_block(free_seed, self.closed_problems[free_seed.parent])
		except KeyError:
			pass
#			raise KeyError(", ".join([str(item) for item in self.open_problems]))

	def get_highest_blocks(self):
		blocks = list(self.closed_problems.values())
		blocks.sort(key=lambda x: x.height)
		return blocks[:num_highest_nodes_to_return]

	def process_queued_message(self):
		if len(self.message_queue) != 0:
			message_instance = self.message_queue.pop(0)
			if not isinstance(message_instance, message):
				raise TypeError("message_instance should be of type message; currently of type "+str(type(message_instance))+".")

			if message_instance.message_type == "proposal":
				if message_instance.orig_author == self:
					pass
				elif message_instance.orig_author in [x.orig_author for x in self.open_problems]:
					pass
				else:
					self.open_problems.add(message_instance)
					for neigh in self.neighbors:
						if neigh != self:
							neigh.message_queue.append(message_instance)

			if message_instance.message_type == "solution":
				temp_list = list(self.closed_problems.keys())
				if message_instance.block not in temp_list:
					if message_instance.block.parent in temp_list:
						if message_instance.orig_author in [x.orig_author for x in self.open_problems]:
							self.open_problems.remove(self.find_prob_message_by_author(message_instance.orig_author))
						self.add_fixed_block(message_instance)
						if message_instance.orig_author == self:
							self.problem_proposed = False
						for neigh in self.neighbors:
							if neigh != self:
								neigh.message_queue.append(message_instance)

	def pass_message(self, message_instance, other):
		if not isinstance(message_instance, message):
			raise TypeError("message_instance should be of type message; currently of type "+str(type(message_instance))+".")

		if message_instance.message_type == "proposal":
			if message_instance.orig_author == other:
				pass
			elif message_instance.orig_author in [x.orig_author for x in other.open_problems]:
				pass
			else:
				other.open_problems.add(message_instance)
				for neigh in other.neighbors:
					if neigh != self:
						other.pass_message(message_instance, neigh)

		if message_instance.message_type == "solution":
			temp_list = list(other.closed_problems.keys())
			if message_instance.block not in temp_list:
				if message_instance.block.parent in temp_list:
					if message_instance.orig_author in [x.orig_author for x in other.open_problems]:
						other.open_problems.remove(other.find_prob_message_by_author(message_instance.orig_author))
					other.add_fixed_block(message_instance)
					if message_instance.orig_author == other:
						other.problem_proposed = False
					for neigh in other.neighbors:
						if neigh != self:
							other.pass_message(message_instance, neigh)

class cooperative_wrapper(universe_wrapper):
	def __init__(self, universe, percentage_update_action=0.1):
		super().__init__(universe, percentage_update_action)
		if not all(isinstance(item, cooperative_node) for item in self.universe):
			raise TypeError("All nodes in a cooperative_wrapper instance must be of cooperative_node type.")

		self.next_block_id = 1

	def get_next_block_id(self):
		to_return = self.next_block_id
		self.next_block_id += 1
		return to_return

	def bestow_block(self):
		cond = False
		count = 0
		while not cond:
			winner = choice(list(self.universe))
			if len(winner.open_problems) != 0:
				cond = True
			elif count == 1000:
				raise ValueError("Excessive runtime in first while loop of bestow_block")
			count += 1
		cond = False
		count = 0
		while not cond:
			solved_problem = choice(list(winner.open_problems))
			if solved_problem.orig_author != winner:
				cond = True
			elif count == 1000:
				raise ValueError("Excessive runtime in first while loop of bestow_block")
			count += 1
		winner.add_fixed_block(solved_problem)
		for neigh in winner.neighbors:
			neigh.message_queue.append(message(solved_problem.block, "solution", solved_problem.orig_author, winner))
#			winner.pass_message(message(solved_problem.block, "solution", solved_problem.orig_author, winner), neigh)

	def pose_problems(self):
		for node in self.universe:
			if not node.problem_posed:
				node.problem_posed = True
				new_free_block = free_block(self.get_next_block_id(), node.get_highest_blocks()[0].block)
				prob_message = message(new_free_block, "proposal", node)
				for neigh in node.neighbors:
					neigh.message_queue.append(prob_message)
#					node.pass_message(prob_message, neigh)

def make_cooperative_wrapper(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
	universe = set()
	for j in range(num_nodes):
		universe.add(cooperative_node("node_"+str(j), universe, add_behavior=add_behavior, drop_behavior=drop_behavior, pass_prob=pass_prob, get_add_prob=get_add_prob))
	return cooperative_wrapper(universe)
