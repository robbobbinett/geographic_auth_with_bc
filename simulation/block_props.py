class free_block:
	"""
	The primitive for a block (i.e. a nonce-satisfied problem that is
	acceptable for committing to a local blockchain
	"""
	def __init__(self, unique_id, parent=None):
		if not isinstance(unique_id, int):
			raise TypeError("parent must be of type free_block; currently of type "+str(type(parent))+".")
		if not isinstance(parent, free_block):
			if unique_id == 0:
				if parent is not None:
					raise TypeError("If unique_id is 0, then parent should be None.")
			else:
				raise TypeError("parent must be of type free_block; currently of type "+str(type(parent))+".")
		if unique_id == 0 and parent is not None:
			raise TypeError("If unique_id is 0, then parent should be None.")

		self.id = unique_id
		self.parent = parent

	def __str__(self):
		return "Free Block\nID: "+str(self.id)+"\nParent ID: "+str(self.parent.id)+"\n"

	def __disp__(self):
		return str(self)

	def __hash__(self):
		"""
		Hashing by self.id allows for inclusion in sets, easy dict mapping, etc.
		"""
		return hash(self.id)

	def __eq__(self, other):
		"""
		For equality to hold, both names and parents must be identical
		"""
		if not isinstance(other, free_block):
			raise TypeError("other must be of type free_block; currently of type "+str(type(other))+".")
		return self.id == other.id and self.parent == other.parent

null_block = free_block(0)

class fixed_block:
	"""
	Primitive for taking a valid block (to be committed to a local blockchain)
	and installing it into a local chain. Creates a rooted tree structure
	"""
	def __init__(self, free_seed, parent=None):
		if not isinstance(free_seed, free_block):
			raise TypeError("free_seed must be of type free_block; currently of type "+str(type(free_seed))+".")
		self.block = free_seed

		if not isinstance(parent, fixed_block):
			if self.block == null_block:
				if parent is not None:
					raise TypeError("If free_seed is the null_block, then parent must be None; parent is currently of type "+str(type(parent))+".")
			else:
				raise TypeError("parent must be of type fixed_block; currently of type "+str(type(parent))+".")
		self.parent = parent

		# self.height is the number of inheritances (parent-child
		# relationships) from root to self.
		if self.parent is None:
			self.height = 0
		else:
			self.height = parent.height + 1

		# list of child nodes, which is updated and sorted by
		# self.block.id
		self.children = []

		# self.shoulder_weight is the number of nodes which, by
		# transitivity of childhood, inherit from self. computed
		# using self.cascading_shoulder_weight_add
		self.shoulder_weight = 0

	def cascading_shoulder_weight_add(self):
		"""
		Every time a child node is appended, increase by 1 the shoulder
		weight of all nodes from whom the new node receives inheritance
		"""
		self.shoulder_weight += 1
		if self.parent is not None:
			self.parent.cascading_shoulder_weight_add()

	def add_child(self, free_child):
		"""
		Insert a child node into tree, and update the parameters of all
		parent/child nodes accordingly
		"""
		if not isinstance(free_child, free_block):
			raise TypeError("child must be of type free_block; currently of type "+str(type(child))+".")
		fixed_child = fixed_block(free_child, self)
		self.children.append(fixed_child)
		self.children.sort(key=lambda x: str(x.block))
		self.cascading_shoulder_weight_add()
		return fixed_child

	def get_root(self):
		"""
		Get root of the current tree.
		"""
		if self.parent is None:
			return self
		else:
			return self.parent.get_root()

	def __eq__(self, other):
		"""
		self == other iff self.block == other.block
		"""
		if not isinstance(other, fixed_block):
			raise TypeError("other should be of type fixed_block; currently of type "+str(type(other))+".")
		return self.block == other.block
