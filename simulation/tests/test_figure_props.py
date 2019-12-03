from figure_props import get_longest_chain_hist
from message_props import *
from node_extensions import *

def test_get_longest_chain_hist():
	"""
	Write better docstring later
	"""
	chance_the = make_cooperative_wrapper(3)
	for node in chance_the.universe:
		for other_node in chance_the.universe:
			if node != other_node:
				node.neighbors.add(other_node)

	for _ in range(10):
		chance_the.pose_problems()
		for _ in range(27):
			chance_the.process_queues()
		chance_the.bestow_block()
		for _ in range(27):
			chance_the.process_queues()
		longest_chain_hist = get_longest_chain_hist(chance_the)
		longest_chain_hist_keys = list(longest_chain_hist.keys())
		assert len(longest_chain_hist_keys) == 1
		assert longest_chain_hist[longest_chain_hist_keys[0]] == 1
