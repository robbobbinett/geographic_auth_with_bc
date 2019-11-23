from message_props import *
from tqdm import tqdm
import numpy as np

def test_cooperative_wrapper_doesnt_crash():
	"""
	Run all methods of the universe_wrapper class (which in turn
	runs all methods of the person_node class). The size of the
	universe should hopefully preclude (in probability) errors
	arising
	"""
	universe = make_cooperative_wrapper(100)

	# Running 1000 position updates per node on each node in a 1000-node universe
	for _ in tqdm(range(1000)):
		universe.run_update()

	# Try bestowing a block; should raise an error due to lack of open problem instances
	try:
		universe.bestow_block()
		assert False
	except ValueError:
		pass

	# Try alternating node updates and block bestowals
	for _ in tqdm(range(1000)):
		universe.pose_problems()
		for _ in range(100):
			universe.process_queues()
		try:
			universe.bestow_block()
		except ValueError:
			raise ValueError("mean open_problems size: "+str(np.mean([len(node.open_problems) for node in universe.universe])))
		for _ in range(100):
			universe.process_queues()

	test_mat = universe.output_connections()

def test_specific_cooperative_wrapper():
	"""
	Cooperative wrapper with three cooperative nodes;
	Nodes are forced to all be neighbors (full clique).
	"""
	chance_the = make_cooperative_wrapper(3)
	for node in chance_the.universe:
		for other_node in chance_the.universe:
			if node != other_node:
				node.neighbors.add(other_node)

	# Check that local blockchains are "minimal" to begin with
	for node in chance_the.universe:
		root = node.closed_problems[null_block]
		assert root.block == null_block
		assert len(root.children) == 0

	# Try alternating node updates and block bestowals
	for node in chance_the.universe:
		assert len(node.open_problems) == 0
	chance_the.pose_problems()
	for node in chance_the.universe:
		assert len(node.open_problems) == 1
		assert list(node.open_problems.values())[0].orig_author == node
	for _ in range(5):
		chance_the.process_queues()
	for node in chance_the.universe:
		assert len(node.open_problems) == 3, "There are "+str(len(node.open_problems))+" open problems:"+"\n".join(str(problem) for problem in node.open_problems)
		for other_node in chance_the.universe:
			assert other_node in [message.orig_author for message in node.open_problems.values()]
	chance_the.bestow_block()
	for _ in range(5):
		chance_the.process_queues()
	for node in chance_the.universe:
		root = node.closed_problems[null_block]
		assert root.block == null_block
		assert len(root.children) == 1, "For node "+str(node)+", root.children is of length "+str(len(root.children))+" and node.closed_problems is of length "+str(len(node.closed_problems))+". Further, node.message_queue is of length "+str(len(node.message_queue))+". Further, the top message in node.message_queue looks like "+str(node.message_queue[0])
		assert len(root.children[0].children) == 0
		assert len(node.message_queue) == 0
