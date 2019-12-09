from tqdm import tqdm
from message_props import cooperative_wrapper, BestowBlockTimeoutError
from coop_tor_node import make_coop_tor_wrapper
from figure_props import get_chain_hist, get_longest_chain_hist, get_leaf_hist

def run_message_cycle(wrapper_instance, chain_hist_store=None, longest_chain_hist_store=None, leaf_hist_store=None, forgive_timeout=False):
	"""
	Run a single cycle of message updates:
	1) Pose Questions
	2) Empty Queues
	3) Bestow Block
	4) Exhaust Queues
	5) Store State Information
	"""
	# 1) Pose Questions
	wrapper_instance.pose_problems()
	# 2) Empty Queues
	wrapper_instance.empty_queues()
	# 3) Bestow Block
	if not forgive_timeout:
		wrapper_instance.bestow_block()
	else:
		try:
			wrapper_instance.bestow_block()
		except BestowBlockTimeoutError:
			pass
	# 4) Exhaust Queues
	wrapper_instance.empty_queues()
	# 5) Store State Information
	for store, fun in zip([chain_hist_store, longest_chain_hist_store, leaf_hist_store], [get_chain_hist, get_longest_chain_hist, get_leaf_hist]):
		if store is not None:
			store.append(fun(wrapper_instance))

def standard_routine(wrapper_instance, num_cycles, message_cycles_per_update_action, chain_hist_store=None, longest_chain_hist_store=None, leaf_hist_store=None, adj_mat_store=None, forgive_timeout=False):
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
		if (j % message_cycles_per_update_action) == 0:
			wrapper_instance.run_update()
			if adj_mat_store is not None:
				adj_mat_store.append(wrapper_instance.output_connections())
		run_message_cycle(wrapper_instance, chain_hist_store=chain_hist_store, longest_chain_hist_store=longest_chain_hist_store, leaf_hist_store=leaf_hist_store, forgive_timeout=forgive_timeout)
