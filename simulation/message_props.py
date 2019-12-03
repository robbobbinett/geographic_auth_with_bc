from random import choice, sample
from node_props import *
from block_props import *

message_types = ["proposal", "solution"]

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

	def __str__(self):
		return "\n".join(str(item) for item in [self.block, self.message_type, self.orig_author])

class cooperative_node(person_node):
	def __init__(self, name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
		super().__init__(name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob)
		self.open_problems = {}
		self.closed_problems = {null_block: fixed_block(null_block)}
		self.problem_posed = False
		self.message_queue = []

	def find_prob_message_by_author(self, orig_author):
		for x in self.open_problems.values():
			if x.orig_author == orig_author:
				return x
		raise KeyError("unrecognized orig_author")

	def add_fixed_block(self, message_instance):
		free_seed = message_instance.block
		try:
			del self.open_problems[free_seed]
		except KeyError:
			raise KeyError("self.open_problems have the following keys: "+", ".join(str(key) for key in self.open_problems.keys())+". The unrecognized key was: "+str(free_seed)+".")
		self.closed_problems[free_seed] = self.closed_problems[free_seed.parent].add_child(free_seed)

	def get_highest_blocks(self):
		blocks = list(self.closed_problems.values())
		blocks.sort(key=lambda x: x.height, reverse=True)
		return [block for block in blocks if block.height == blocks[0].height]

	def process_queued_message(self):
		if len(self.message_queue) != 0:
			message_instance = self.message_queue.pop(0)
			if not isinstance(message_instance, message):
				raise TypeError("message_instance should be of type message; currently of type "+str(type(message_instance))+".")

			if message_instance.message_type == "proposal":
				if message_instance.block in self.closed_problems:
					pass
				elif message_instance.orig_author == self:
					pass
				elif message_instance.block in self.open_problems:
					pass
				else:
					if message_instance.orig_author in [x.orig_author for x in self.open_problems.values()]:
						del self.open_problems[self.find_prob_message_by_author(message_instance.orig_author).block]
					self.open_problems[message_instance.block] = message_instance
					for neigh in self.neighbors:
						if neigh != self:
							neigh.message_queue.append(message_instance)

			if message_instance.message_type == "solution":
				temp_list = list(self.closed_problems.keys())
				other_temp_list = list(self.open_problems.keys())
				if message_instance.block not in temp_list and message_instance.block in other_temp_list:
					if message_instance.block.parent in temp_list:
						self.add_fixed_block(message_instance)
						if message_instance.orig_author == self:
							self.problem_posed = False
						for neigh in self.neighbors:
							neigh.message_queue.append(message_instance)

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
			if len(winner.open_problems) == 0:
				pass
			else:
				solved_problem = choice(list(winner.open_problems.values()))
				if solved_problem.orig_author != winner:
					cond = True
			if count == 1000:
				raise ValueError("Excessive runtime in second while loop of bestow_block")
			count += 1
		winner.problem_proposed = False
		winner.add_fixed_block(solved_problem)
		for neigh in winner.neighbors:
			neigh.message_queue.append(message(solved_problem.block, "solution", solved_problem.orig_author, winner))

	def pose_problems(self):
		for node in self.universe:
			if not node.problem_posed:
				node.problem_posed = True
				new_free_block = free_block(self.get_next_block_id(), node.get_highest_blocks()[0].block)
				prob_message = message(new_free_block, "proposal", node)
				node.open_problems[new_free_block] = prob_message
				for neigh in node.neighbors:
					neigh.message_queue.append(prob_message)

	def process_queues(self):
		for node in self.universe:
			node.process_queued_message()

	def count_num_longest_chains(self):
		# NOTE: Each unique chain can be uniquely identified by its highest block's ID
		highest_block_counter = {}
		for node in self.universe:
			highest_blocks = node.get_highest_blocks()
			for block in highest_blocks:
				try:
					highest_block_counter[block] += 1
				except KeyError:
					highest_block_counter[block] = 1
		return highest_block_counter

	def empty_queues(self):
		"""
		Call self.process_queues until no more messages are propagating through the network
		"""
		cond = False
		while not cond:
			self.process_queues()
			cond = all([len(node.message_queue) == 0 for node in self.universe])

def make_cooperative_wrapper(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
	universe = set()
	for j in range(num_nodes):
		universe.add(cooperative_node("node_"+str(j), universe, add_behavior=add_behavior, drop_behavior=drop_behavior, pass_prob=pass_prob, get_add_prob=get_add_prob))
	return cooperative_wrapper(universe)
