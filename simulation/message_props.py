from node_props import *

message_denoms = ["null", "problem_proposal", "tentative_solution", "problem_solved"]

class message:
	"""
	Parent class for all kinds of messages to be passed between nodes
	"""
	def __init__(self, author, orig_timestamp, denom="null"):
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
