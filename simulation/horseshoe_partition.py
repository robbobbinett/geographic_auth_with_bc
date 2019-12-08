from message_props import make_cooperative_wrapper
from figure_props import *

# Create the following topology
# 1 ---- 2
# |      |
# |      |
# 0      3

# Run enough time to generate and propagate 50 blocks
chance_the = make_cooperative_wrapper(4)
to_pair = [(0, 1), (1, 2), (2, 3)]
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) in to_pair:
			node.neighbors.add(other_node)
			other_node.neighbors.add(node)

# collect longest chains
hist_list = []

for _ in range(50):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))

# Partition the topology into the following
# 1      2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 50 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.remove(other_node)
			other_node.neighbors.remove(node)

for _ in range(50):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))

# Rejoin the topology into the following
# 1 ---- 2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 50 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.add(other_node)
			other_node.neighbors.add(node)

for _ in range(50):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))

global_chain_adherence_graph([node.get_root_block() for node in chance_the.universe], "horseshoe")
for j, quasi_root in enumerate([node.get_root_block() for node in chance_the.universe]):
	visualize_subtree(quasi_root, filename="horseshoe_"+str(j))

heatmap_from_hists(hist_list)
