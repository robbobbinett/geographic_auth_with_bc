from block_props import *

def test_free_block_creation():
	"""
	Test that block creation succeeds and fails as desired. Also guarantee
	equality based on both self.id and self.parent.id
	"""
	# The following should fail, due to that null_block != None
	try:
		free_block(0, null_block)
		assert False
	except TypeError:
		assert True

	# The following should pass, and should be equal to null_block
	temp_block = free_block(0, None)
	assert temp_block == null_block

	# The following test blocks share the same name but have different parents
	# Therefore, they should not be equal
	temp1 = free_block(1, null_block)
	temp2 = free_block(1, temp1)
	assert temp1 != temp2

def test_fixed_block_tree_formation():
#	assert True
	"""
	Test that the fixed_block primitive creates trees in the expected
	fashion; tested using toy tree examples.
	"""
	# The one-node rooted tree
	root = fixed_block(null_block)
	assert root.height == 0
	assert root.get_root() == root
	assert root.shoulder_weight == 0
	assert root.children == []

	# The ten-node (rooted) path
	prev_free_block = null_block
	prev_fixed_block = root
	fixed_block_book = {0: prev_fixed_block}
	for j in range(1, 10):
		curr_fixed_block = prev_fixed_block.add_child(free_block(j, prev_free_block))
		prev_fixed_block = curr_fixed_block
		prev_free_block = curr_fixed_block.block
		fixed_block_book[j] = prev_fixed_block
	for j in range(10):
		temp_block = fixed_block_book[j]
		assert temp_block.height == j
		assert temp_block.get_root() == root
		assert temp_block.shoulder_weight == 9-j
		assert temp_block.children == ([fixed_block_book[j+1]] if j != 9 else [])

	# The following rooted tree
	#
	# o  o
	# | /
	# o  o
	# | /
	# o
	# |
	# o
	# |
	# o    o
	# |   /
	# o  o
	# | /
	# o
	# |
	# o  o
	# | /
	# o  o
	# | /
	# o
	#
	# NOTE: As the original nodes have IDs 0-9, these new nodes will
	# be labeled 10-15, from smallest-to-highest height.
	fixed_block_book[10] = root.add_child(free_block(10, null_block))
	fixed_block_book[11] = fixed_block_book[1].add_child(free_block(11, fixed_block_book[1].block))
	fixed_block_book[12] = fixed_block_book[3].add_child(free_block(12, fixed_block_book[3].block))
	fixed_block_book[13] = fixed_block_book[12].add_child(free_block(13, fixed_block_book[12].block))
	fixed_block_book[14] = fixed_block_book[7].add_child(free_block(14, fixed_block_book[7].block))
	fixed_block_book[15] = fixed_block_book[8].add_child(free_block(15, fixed_block_book[8].block))

	# Record actual heights manually
	heights = dict((j,j) for j in range(10))
	heights[10] = 1
	heights[11] = 2
	heights[12] = 4
	heights[13] = 5
	heights[14] = 8
	heights[15] = 9
	# Check heights
	for j in range(16):
		assert fixed_block_book[j].height == heights[j]
	# Check leaf properties
	for j in [9, 10, 11, 13, 14, 15]:
		temp_block = fixed_block_book[j]
		assert temp_block.get_root() == root
		assert temp_block.shoulder_weight == 0
		assert temp_block.children == []

	# Check that root records total weight of nodes above, that node 1
	# is this weight minus two
	assert root.shoulder_weight == 15
	assert fixed_block_book[1].shoulder_weight == 13

	# Check that fixed_block.return_bfs returns an appropriate ordering of nodes
	list_of_nodes = root.return_bfs()
	assert len(list_of_nodes) == 16
	for j in range(len(list_of_nodes)-1):
		assert list_of_nodes[j].height <= list_of_nodes[j+1].height
