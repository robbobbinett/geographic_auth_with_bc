from message_props import *
from node_extensions import *
from coop_tor_node import *
from rigged_rng import make_rigged_rng
from tqdm import tqdm
import numpy as np
import math
import random

def test_coop_tor_nodes():
	rng_values = []
	rng = make_rigged_rng(rng_values)
	universe = set()
	r = 0.15
	s = 0.1

	# Basic node creation
	rng_values.extend([0.3, 0.1])
	n1 = coop_tor_node("n1", universe, r, s, rng)
	universe.add(n1)
	assert math.isclose(n1.x, 0.3)
	assert math.isclose(n1.y, 0.1)

	# Node movement
	rng_values.append(0.0) # movement angle, divided by 2*pi
	n1.move()
	assert math.isclose(n1.x, 0.4)
	assert math.isclose(n1.y, 0.1)

	rng_values.append(0.5)
	n1.move()
	assert math.isclose(n1.x, 0.3)
	assert math.isclose(n1.y, 0.1)

	rng_values.append(0.25)
	n1.move()
	assert math.isclose(n1.x, 0.3)
	assert math.isclose(n1.y, 0.2)

	rng_values.append(0.75)
	n1.move()
	assert math.isclose(n1.x, 0.3)
	assert math.isclose(n1.y, 0.1)

	# Toroidal movement
	rng_values.extend([0.75, 0.75])
	n1.move()
	n1.move()
	assert math.isclose(n1.x, 0.3)
	assert math.isclose(n1.y, 0.9)

	rng_values.extend([0.5, 0.5, 0.5, 0.5])
	n1.move()
	n1.move()
	n1.move()
	n1.move()
	assert math.isclose(n1.x, 0.9)
	assert math.isclose(n1.y, 0.9)

	rng_values.extend([0.25, 0.25])
	n1.move()
	n1.move()
	assert math.isclose(n1.x, 0.9)
	assert math.isclose(n1.y, 0.1)

	rng_values.extend([0, 0])
	n1.move()
	n1.move()
	assert math.isclose(n1.x, 0.1)
	assert math.isclose(n1.y, 0.1)

	# Creating a second node, testing connectivity
	rng_values.extend([0.2, 0.2])
	n2 = coop_tor_node("n2", universe, r, s, rng)
	universe.add(n2)
	assert math.isclose(n2.x, 0.2)
	assert math.isclose(n2.y, 0.2)

	n2.update_neighbors()
	assert n2.neighbors == {n1}
	assert n1.neighbors == {n2}

	# Test connectivity after movement
	rng_values.append(0.125)
	n2.move()
	n2.update_neighbors()
	assert n2.neighbors == set()
	assert n1.neighbors == set()

	# Test node update
	rng_values.append(0.625)
	n2.update_action()
	assert n2.neighbors == {n1}
	assert n1.neighbors == {n2}

	# Make universe with more nodes
	rng_values.extend([0.3, 0.2, 0.4, 0.1])
	n3 = coop_tor_node("n3", universe, r, s, rng)
	universe.add(n3)
	n4 = coop_tor_node("n4", universe, r, s, rng)
	universe.add(n4)
	n3.update_neighbors()

	assert n1.neighbors == {n2}
	assert n2.neighbors == {n1, n3}
	assert n3.neighbors == {n2, n4}
	assert n4.neighbors == {n3}

	# Move the two cliques away from each other
	wrapped_universe = cooperative_wrapper(universe, 1.0)
	rng_values.extend([0.5, 0.5, 0.0, 0.0])
	wrapped_universe.run_update()
	assert math.isclose(n1.x, 0.0)
	assert math.isclose(n1.y, 0.1)
	assert math.isclose(n2.x, 0.1)
	assert math.isclose(n2.y, 0.2)
	assert math.isclose(n3.x, 0.4)
	assert math.isclose(n3.y, 0.2)
	assert math.isclose(n4.x, 0.5)
	assert math.isclose(n4.y, 0.1)
	assert n1.neighbors == {n2}
	assert n2.neighbors == {n1}
	assert n3.neighbors == {n4}
	assert n4.neighbors == {n3}

	# Move the two cliques back
	rng_values.extend([0.0, 0.0, 0.5, 0.5])
	wrapped_universe.run_update()
	assert math.isclose(n1.x, 0.1)
	assert math.isclose(n1.y, 0.1)
	assert math.isclose(n2.x, 0.2)
	assert math.isclose(n2.y, 0.2)
	assert math.isclose(n3.x, 0.3)
	assert math.isclose(n3.y, 0.2)
	assert math.isclose(n4.x, 0.4)
	assert math.isclose(n4.y, 0.1)
	assert n1.neighbors == {n2}
	assert n2.neighbors == {n1, n3}
	assert n3.neighbors == {n2, n4}
	assert n4.neighbors == {n3}

def test_toroidal_universe_maker():
	rng_values = [0.0, 0.0, 0.1, 0.1, 0.2, 0.1, 0.3, 0.0]
	torus = make_torus_of_nodes(4, 0.15, 0.1, make_rigged_rng(rng_values))
	n1 = torus.name_to_node['toroidal_node_0']
	n2 = torus.name_to_node["toroidal_node_1"]
	n3 = torus.name_to_node["toroidal_node_2"]
	n4 = torus.name_to_node["toroidal_node_3"]
	assert math.isclose(n1.x, 0.0)
	assert math.isclose(n1.y, 0.0)
	assert math.isclose(n2.x, 0.1)
	assert math.isclose(n2.y, 0.1)
	assert math.isclose(n3.x, 0.2)
	assert math.isclose(n3.y, 0.1)
	assert math.isclose(n4.x, 0.3)
	assert math.isclose(n4.y, 0.0)
	assert n1.neighbors == {n2}
	assert n2.neighbors == {n1, n3}
	assert n3.neighbors == {n2, n4}
	assert n4.neighbors == {n3}

def test_make_coop_tor_wrapper_with_default_rng():
	universe = make_coop_tor_wrapper(150, 0.1, 0.01, random.random)

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
