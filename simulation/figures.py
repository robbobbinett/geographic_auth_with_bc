from random import choice
from tqdm import tqdm
from node_props import *
from wrapper_props import *
from node_extensions import *
from block_props import *
from message_props import *
from figure_props import *

num_nodes = 3

#chance_the = make_cooperative_wrapper(num_nodes, add_behavior=full_clique_add, drop_behavior=full_clique_drop, pass_prob=0.5, get_add_prob=lambda x: 1.0)
chance_the = make_full_clique(num_nodes)

for node in chance_the.universe:
	assert len(node.neighbors) == 2

# Bestow blocks and stuff
for _ in tqdm(range(100)):
	chance_the.pose_problems()
	for _ in range(10):
		chance_the.process_queues()
	for node in chance_the.universe:
		assert len(node.open_problems) in [2, 3], "We have this many open problems: "+str(len(node.open_problems))
	chance_the.bestow_block()
	for _ in range(10):
		chance_the.process_queues()

#test_node = choice(list(chance_the.universe))
#visualize_subtree(test_node.closed_problems[null_block])

for j, node in enumerate(chance_the.universe):
	visualize_subtree(node.closed_problems[null_block], filename="node_"+str(j))
