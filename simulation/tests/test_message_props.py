from message_props import *
from node_extensions import *
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
	for _ in tqdm(range(100)):
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
	for _ in range(100):
		chance_the.process_queues()
	for node in chance_the.universe:
		root = node.closed_problems[null_block]
		assert root.block == null_block
		assert len(root.children) == 1, "For node "+str(node)+", root.children is of length "+str(len(root.children))+" and node.closed_problems is of length "+str(len(node.closed_problems))+". Further, node.message_queue is of length "+str(len(node.message_queue))+". Further, the top message in node.message_queue looks like "+str(node.message_queue[0])
		assert len(root.children[0].children) == 0

def test_full_clique():
	"""
	Test full clique of three nodes.
	"""
	num_nodes = 3
	chance_the = make_full_clique(num_nodes)
	for node in chance_the.universe:
		assert len(node.neighbors) == 2
		assert len(node.open_problems) == 0
		assert len(node.closed_problems) == 1

	for j in tqdm(range(10)):
		chance_the.pose_problems()
		for _ in range(100):
			chance_the.process_queues()
		for node in chance_the.universe:
			assert len(node.message_queue) == 0, "In round "+str(j)+", though a message queue should be empty, it contains messages of types: "+", ".join(item.message_type for item in node.message_queue)
		for node in chance_the.universe:
			for other in chance_the.universe:
				for key in node.open_problems.keys():
					assert key in other.open_problems, "In round "+str(j)+", the open-problem key "+str(key)+" is in node "+str(node)+" but not node "+str(other)
		for node in chance_the.universe:
			assert len(node.open_problems) == 3, "In iteration "+str(j)+", found that a node had this many open problems: "+str(len(node.open_problems))+". Of these open problems, this many were self: "+str(len([1 for prob in node.open_problems.values() if prob.orig_author == node]))
		chance_the.bestow_block()
		for _ in range(100):
			chance_the.process_queues()
		for k, node in enumerate(chance_the.universe):
			assert len(node.closed_problems) == j+2, "In iteration "+str(j)+", found that a node had this many closed problems: "+str(len(node.closed_problems))+". Of these, the heights are: "+", ".join([str(item.height) for item in node.closed_problems.values()])+". This was the "+str(k)+"th node checked."
		for node in chance_the.universe:
			for other in chance_the.universe:
				for key in node.closed_problems.keys():
					assert key in other.closed_problems, "In round "+str(j)+", the closed-problem key "+str(key)+" is in node "+str(node)+" but not node "+str(other)
