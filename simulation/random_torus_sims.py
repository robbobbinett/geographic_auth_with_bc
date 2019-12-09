from itertools import product
import random
from tqdm import tqdm
from message_props import cooperative_wrapper
from coop_tor_node import make_coop_tor_wrapper

def run_message_cycle(wrapper_instance):
	"""
	Run a single cycle of message updates:
	1) Pose Questions
	2) Empty Queues
	3) Bestow Block
	4) Exhaust Queues
	"""
#	1) Pose Questions
	wrapper_instance.pose_problems()
#	2) Empty Queues
	wrapper_instance.empty_queues()
#	3) Bestow Block
	wrapper_instance.bestow_block()
#	4) Exhaust Queues
	wrapper_instance.empty_queues()

def standard_routine(wrapper_instance, num_cycles, message_cycles_per_update_action):
	"""
	The standard simulation routine through which all the wrappers are to be
	simulated.
	"""
	# Check type conformity
	if not isinstance(wrapper_instance, cooperative_wrapper):
		raise TypeError("wrapper_instance should be of type cooperative_wrapper; currently of type "+str(type(wrapper_instance)))
	for name, var in zip(["num_cycles", "message_cycles_per_update_action"], [num_cycles, message_cycles_per_update_action]):
		if not isinstance(var, int):
			raise TypeError(name+" should be of type int; currently of type "+str(type(var)))

	# Run message cycles, with update_action calls periodically interspersed
	for j in tqdm(range(num_cycles)):
		run_message_cycle(wrapper_instance)
		if (j != 0) and (j % message_cycles_per_update_action) == 0:
			wrapper_instance.run_update()

sizes = [10, 50, 100]
rs = [0.05, 0.1, 0.25, 0.5]
ss = [0.05, 0.1, 0.15, 0.2]

for size, r, s in product(sizes, rs, ss):
	chance_the = make_coop_tor_wrapper(size, r, s, random.random)
	standard_routine(chance_the, 10, 5)
