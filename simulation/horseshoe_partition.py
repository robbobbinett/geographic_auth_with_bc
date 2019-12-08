from message_props import make_cooperative_wrapper
from figure_props import *

# Create the following topology
# 1 ---- 2
# |      |
# |      |
# 0      3

# Run enough time to generate and propagate 10 blocks
chance_the = make_cooperative_wrapper(4)
to_pair = [(0, 1), (1, 2), (2, 3)]
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) in to_pair:
			node.neighbors.add(other_node)
			other_node.neighbors.add(node)

# collect longest chains
hist_list = []
# Collect leaves
leaf_book = {}
for j, node in enumerate(list(chance_the.universe)):
	leaf_book[j] = []

for _ in range(10):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))
	for j, node in enumerate(list(chance_the.universe)):
		leaf_book[j].append([block.height for block in node.get_leaf_blocks()])

# Partition the topology into the following
# 1      2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 10 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.remove(other_node)
			other_node.neighbors.remove(node)

for _ in range(10):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))
	for j, node in enumerate(list(chance_the.universe)):
		leaf_book[j].append([block.height for block in node.get_leaf_blocks()])

# Rejoin the topology into the following
# 1 ---- 2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 10 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.add(other_node)
			other_node.neighbors.add(node)

for _ in range(10):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))
	for j, node in enumerate(list(chance_the.universe)):
		leaf_book[j].append([block.height for block in node.get_leaf_blocks()])

# Partition the topology into the following
# 1      2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 10 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.remove(other_node)
			other_node.neighbors.remove(node)

for _ in range(10):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))
	for j, node in enumerate(list(chance_the.universe)):
		leaf_book[j].append([block.height for block in node.get_leaf_blocks()])

# Rejoin the topology into the following
# 1 ---- 2
# |      |
# |      |
# 0      3

# Run enought time to generate and propagate 10 blocks
for j, node in enumerate(chance_the.universe):
	for k, other_node in enumerate(chance_the.universe):
		if (j, k) == (1, 2):
			node.neighbors.add(other_node)
			other_node.neighbors.add(node)

for _ in range(10):
	chance_the.pose_problems()
	chance_the.empty_queues()
	chance_the.bestow_block()
	chance_the.empty_queues()
	hist_list.append(get_leaf_hist(chance_the))
	for j, node in enumerate(list(chance_the.universe)):
		leaf_book[j].append([block.height for block in node.get_leaf_blocks()])

global_chain_adherence_graph([node.get_root_block() for node in chance_the.universe], "horseshoe")
for j, quasi_root in enumerate([node.get_root_block() for node in chance_the.universe]):
	visualize_subtree(quasi_root, filename="horseshoe_"+str(j))

heatmap_from_hists(hist_list)
for key in leaf_book.keys():
#	violins_from_leaves([leaf_book[key][j] for j in range(30) if j%5 == 0])
	new_books = []
	for book in leaf_book[key]:
		new_book = {}
		for height in book:
			try:
				new_book[height] += 1
			except KeyError:
				new_book[height] = 1
		new_books.append(new_book)
	heatmap_from_hists(new_books)
