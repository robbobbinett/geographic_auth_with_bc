from figure_props import *
from block_props import *
from node_extensions import make_full_clique
from tqdm import tqdm
import matplotlib.pyplot as plt

"""
Test that the fixed_block primitive creates trees in the expected
fashion; tested using toy tree examples.
"""
# The one-node rooted tree
root = fixed_block(null_block)

# The ten-node (rooted) path
prev_free_block = null_block
prev_fixed_block = root
fixed_block_book = {0: prev_fixed_block}
for j in range(1, 10):
	curr_fixed_block = prev_fixed_block.add_child(free_block(j, prev_free_block))
	prev_fixed_block = curr_fixed_block
	prev_free_block = curr_fixed_block.block
	fixed_block_book[j] = prev_fixed_block

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

visualize_subtree(root, filename="test_0")

"""
Test full clique of three nodes.
"""
ranges = [10, 50, 100]

for lagrange in ranges:
	num_nodes = 3
	chance_the = make_full_clique(num_nodes)
	for node in chance_the.universe:
		assert len(node.neighbors) == 2
		assert len(node.open_problems) == 0
		assert len(node.closed_problems) == 1

	for j in tqdm(range(lagrange)):

		chance_the.pose_problems()
		for _ in range(10):
			chance_the.process_queues()
		for node in chance_the.universe:
			assert len(node.message_queue) == 0, "In round "+str(j)+", though a message queue should be empty, it contains messages of types: "+", ".join(item.message_type for item in node.message_queue)
		for node in chance_the.universe:
			for other in chance_the.universe:
				for key in node.open_problems.keys():
					assert key in other.open_problems, "In round "+str(j)+", the open-problem key "+str(key)+" is in node "+str(node)+" but not node "+str(other)
		for node in chance_the.universe:
			assert len(node.open_problems) == num_nodes, "In iteration "+str(j)+", found that a node had this many open problems: "+str(len(node.open_problems))+". Of these open problems, this many were self: "+str(len([1 for prob in node.open_problems.values() if prob.orig_author == node]))
		chance_the.bestow_block()
		for _ in range(10):
			chance_the.process_queues()
		for k, node in enumerate(chance_the.universe):
			assert len(node.closed_problems) == j+2, "In iteration "+str(j)+", found that a node had this many closed problems: "+str(len(node.closed_problems))+". Of these, the heights are: "+", ".join([str(item.height) for item in node.closed_problems.values()])+". This was the "+str(k)+"th node checked."
		for node in chance_the.universe:
			for other in chance_the.universe:
				for key in node.closed_problems.keys():
					assert key in other.closed_problems, "In round "+str(j)+", the closed-problem key "+str(key)+" is in node "+str(node)+" but not node "+str(other)

	visualize_subtree(list(chance_the.universe)[0].closed_problems[null_block], filename="test_"+str(lagrange))

"""
Test colormap_like plot
"""
ranges = [10, 50]

for lagrange in ranges:
	num_nodes = 30
	chance_the = make_full_clique(num_nodes)
	for node in chance_the.universe:
		assert len(node.neighbors) == num_nodes-1
		assert len(node.open_problems) == 0
		assert len(node.closed_problems) == 1

	list_of_dicts = []

	for j in tqdm(range(lagrange)):

		chance_the.pose_problems()
		chance_the.empty_queues()
		list_of_dicts.append(get_chain_hist(chance_the))
		chance_the.bestow_block()
		chance_the.empty_queues()
		list_of_dicts.append(get_chain_hist(chance_the))

	fig = plt.figure()
	ax = fig.add_subplot(111)
	heatmap_from_hists(list_of_dicts, array_of_times=np.array([(j+1) for j in range(len(list_of_dicts))]), ax=ax)
	fig.savefig("test_outputs/global_chains/"+str(lagrange)+".pdf")

"""
Test formation of union_chains from local chains
"""
# Create the following tree...
# o  o  o
# |  | /
# o  o
# |  |
# o  o
# | /
# o
# |
# o
#
# As the union of the following trees by the function union_of_local_chains:
# o
# |
# o
# |
# o
# |
# o
# |
# o
#
# ----------
#
#    o
#    |
#    o
#    |
#    o
#   /
# o
# |
# o
#
# ----------
#
#       o
#      /
#    o
#    |
#    o
#   /
# o
# |
# o
# Create the tree expected from the union_of_local_chains function
solution_blocks = {0: fixed_block(null_block)}
prev_block = solution_blocks[0]
for j in range(4):
	prev_block = prev_block.add_child(free_block(j+1, prev_block.block))
	solution_blocks[j+1] = prev_block
	prev_block = solution_blocks[1]
for j in range(5, 8):
	prev_block = prev_block.add_child(free_block(j, prev_block.block))
	solution_blocks[j] = prev_block

prev_block = solution_blocks[6]
prev_block = prev_block.add_child(free_block(8, prev_block.block))

# Create each of the local chains to be input into union_of_local_chains
blocks_1 = {0: fixed_block(null_block)}
prev_block = blocks_1[0]
for j in range(4):
	prev_block = prev_block.add_child(free_block(j+1, prev_block.block))
	blocks_1[j+1] = prev_block

blocks_2 = {0: fixed_block(null_block)}
prev_block = blocks_2[0]
prev_block = prev_block.add_child(free_block(1, prev_block.block))
blocks_2[1] = prev_block
for j in range(5, 8):
	prev_block = prev_block.add_child(free_block(j, prev_block.block))
	blocks_2[j] = prev_block

blocks_3 = {0: fixed_block(null_block)}
prev_block = blocks_3[0]
prev_block = prev_block.add_child(free_block(1, prev_block.block))
blocks_3[1] = prev_block
for j in range(5, 7):
	prev_block = prev_block.add_child(free_block(j, prev_block.block))
	blocks_3[j] = prev_block
prev_block = prev_block.add_child(free_block(8, prev_block.block))
blocks_3[8] = prev_block

# union_root = union_of_local_chains([blocks[0] for blocks in [blocks_1, blocks_2, blocks_3]])
union_roots = [blocks[0] for blocks in [blocks_1, blocks_2, blocks_3]]
global_chain_adherence_graph(union_roots, "small_world")
