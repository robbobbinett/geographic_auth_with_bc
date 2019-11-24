from random import choice
from tqdm import tqdm
from node_props import *
from block_props import *
from message_props import *
from figure_props import *

num_nodes = 25

chance_the = make_cooperative_wrapper(num_nodes, add_behavior=default_add, drop_behavior=default_drop, pass_prob=0.5, get_add_prob=default_get_add_prob)

# ALlow for random formation of neighbors
for _ in tqdm(range(1000)):
	chance_the.run_update()

# Bestow blocks and stuff
for _ in tqdm(range(20)):
	chance_the.pose_problems()
	for _ in range(100):
		chance_the.process_queues()
	chance_the.bestow_block()
	for _ in range(100):
		chance_the.process_queues()

test_node = choice(list(chance_the.universe))
visualize_subtree(test_node.closed_problems[null_block])
