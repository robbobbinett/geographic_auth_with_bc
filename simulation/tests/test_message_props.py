from message_props import *
from tqdm import tqdm

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
	for _ in tqdm(range(100)):
		universe.pose_problems()
		for _ in range(100):
			universe.process_queues()
		universe.bestow_block()

	test_mat = universe.output_connections()

def test_specific_cooperative_wrapper():
	"""
	Cooperative wrapper with three cooperative nodes;
	Nodes are forced to all be neighbors (full clique).
	"""
	chance_the = make_cooperative_wrapper(100)
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
	chance_the.pose_problems()
	for _ in range(5):
		chance_the.process_queues()
	chance_the.bestow_block()
	for _ in range(5):
		chance_the.process_queues()
	for node in chance_the.universe:
		root = node.closed_problems[null_block]
		assert root.block == null_block
		assert len(root.children) == 1
		assert len(root.children[0].children) == 0
