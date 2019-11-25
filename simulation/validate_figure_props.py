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
		for _ in range(10):
			chance_the.process_queues()
			list_of_dicts.append(get_longest_chain_hist(chance_the))
		chance_the.bestow_block()
		for _ in range(10):
			chance_the.process_queues()
			list_of_dicts.append(get_longest_chain_hist(chance_the))

	heatmap_from_hists(list_of_dicts, array_of_times=np.array([(j+1) for j in range(len(list_of_dicts))]))
