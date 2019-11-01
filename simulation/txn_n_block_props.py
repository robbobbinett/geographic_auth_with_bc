class free_block:
	def __init__(self, unique_id, parent=None):
		if not isinstance(unique_id, int):
			raise TypeError("parent must be of type free_block; currently of type "+str(type(parent))+".")
		if not isinstance(parent, free_block):
			if unique_id == 0:
				if parent is not None:
					raise TypeError("If unique_id is 0, then parent should be None.")
			else:
				raise TypeError("parent must be of type free_block; currently of type "+str(type(parent))+".")

		self.id = unique_id
		self.parent = parent

	def __str__(self):
		return "Free Block\nID: "+str(self.id)+"\nParent ID: "+str(self.parent.id)+"\n"

	def __disp__(self):
		return str(self)

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if not isinstance(other, free_block):
			raise TypeError("other must be of type free_block; currently of type "+str(type(other))+".")
		return self.id == other.id and self.parent == other.parent

null_block = free_block(0)

class fixed_block:
	def __init__(self, free_seed):
		if not isinstance(free_seed, free_block):
			raise TypeError("free_seed must be of type free_block; currently of type "+str(type(free_seed))+".")
		self.block = free_seed

class local_blockchain:
	"""
	'Nuf said.
	"""
	def __init__(self, seed=None):
		if not seed:
			self.root_node = null_block
			self.weight = 1
			self.height = 1
		elif not isinstance(seed, local_blockchain):
			raise TypeError("seed must be of type local_blockchain; currently of type "+str(type(seed))+".")
		else:
			pass
