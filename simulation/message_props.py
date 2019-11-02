from node_props import *
from block_props import *

message_denoms = ["null", "problem_proposal", "problem_solved"]

class message:
	"""
	Parent class for all kinds of messages to be passed between nodes
	"""
	def __init__(self, author, orig_timestamp, denom="null", self_block=null_block):
		if not isinstance(author, person_node):
			raise TypeError("author must be of type person_node; currently of type "+str(type(author))+".")
		self.orig_author = author

		if not isinstance(orig_timestamp, int):
			raise TypeError("orig_timestamp must be of type int; currently of type "+str(type(orig_timestamp))+".")
		self.orig_timestamp = orig_timestamp

		if denom not in message_denoms:
			if isinstance(denom, str):
				raise ValueError("denom must be one of the following: "+", ".join(message_denoms)+". Currently, denom is "+denom+".")
			else:
				raise ValueError("denom must be of type str; currently of type "+str(type(denom))+".")
		self.denomination = denom

		if not isinstance(self_block, free_block):
			raise TypeError("self_block must be of type free_block; currently of type "+str(type(self_block))+".")
		self.block = self_block

	def __hash__(self):
		"""
		Will only be in a hash table with other messages of same denomination
		"""
		return hash(self.block)

	def __eq__(self, other):
		if not isinstance(other, message):
			raise TypeError("other must be of type message; currently of type "+str(type(other))+".")
		elif self.denomination != other.denomination:
			raise ValueError("self and other must be of same denomination; currently of denominations "+" and ".join([x.denomination for x in (self, other)])+", respectively.")
		else:
			return self.author == other.author and self.timestamp == other.timestamp and self.block == other.block

N = 100

class cooperative_node(person_node):
	"""
	The person_node class, with added message-passing/queueing/processing capability
	"""
	def __init__(self, name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob):
		super().__init__(name, universe, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob)
		for denom in message_denoms:
			setattr(self, denom, set())

	def pass_message(message_instance, recipient):
		if not isinstance(message_instance, message):
			raise TypeError("message_instance must be of type message; currently of type "+str(type(message_instance))+".")
		if not isinstance(recipient, cooperative_node):
			raise TypeError("recipient must be of type cooperative_node; currently of type "+str(type(recipient))+".")

		# Processing null messages
		if message_instance.denomination == "null":
			# For null messages, message author and message passer
			# must be the same.
			if message_instance.orig_author == self:
				# Add to recipient's queue iff message not currently in
				# queue
				other.null.add(message_instance.block)

		# Processing problem_proposal messages
		if message_instance.denomination == "problem_proposal":
			# Can only have N problems enqueued at once
			if len(other.problem_proposal.add) >= N:
				pass
			# For problem_proposal messages, message author and message
			# passer must be the same.
			elif message_instance.orig_author == self:
				# only add to queue iff message author not currently author
				# of another message in queue.
				if self not in [x.orig_author for x in other.problem_proposal]:
					other.problem_proposal.add(message_instance)

		# Processing problem_solved messages
		if message_instance.denomination == "problem_solved":
			# Only entertain if message_instance.self_block is in
			# other.problem_proposal
			if message_instance.self_block in other.problem_proposal:
				other.problem_proposal.remove(message_instance)
				other.problem_solved.add(message_instance.block)
				for neigh in other.neighbors:
					other.pass_message(message_instance, neigh)
			else:
