import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from block_props import fixed_block, union_of_local_chains
from message_props import cooperative_wrapper, cooperative_node

def visualize_subtree(quasi_root, filename=None, scale=None):
	if not isinstance(quasi_root, fixed_block):
		raise TypeError("quasi_root should be of type fixed_block; currently of type "+str(type(fixed_block)))

	if not scale:
		scale = 3.0

	# Get BFS ordering of blocks by height
	blocks_by_height = quasi_root.return_bfs()

	# Get dictionary storing blocks by given height
	height_collection = {}
	for block in blocks_by_height:
		try:
			height_collection[block.height].append(block)
		except KeyError:
			height_collection[block.height] = [block]

	# Count number of blocks of given height
	heights = list(height_collection.keys())
	heights.sort()
	height_dict = dict((key, len(height_collection[key])) for key in heights)

	# Create graphviz nodes for all blocks, starting from quasi_root
	replace1 = ""
	for height in heights:
		width = height_dict[height]
		for j, block in zip(range(width), height_collection[height]):
			replace1 += str(block.block.id)+' [pos="'+str(scale*(j+1)/width)+','+str(-scale*height)+'!"];\n'

	# Draw edges from parents to children
	for block in blocks_by_height:
		for child in block.children:
			replace1 += str(block.block.id) + " -> " + str(child.block.id) + ";\n"

	# Export .dot file
	if not filename:
		filename = str(quasi_root.block.id)
	with open("figure_templates/local_chain_template.txt", "r") as base_file:
		with open ("figure_intermediates/local_chains/"+filename+".dot", "w") as new_file:
			new_file.write(base_file.read().replace('//replace', replace1))

def get_longest_chain_hist(coop_wrapper):
	if not isinstance(coop_wrapper, cooperative_wrapper):
		raise TypeError("coop_wrapper should be of type cooperative_wrapper; currently of type "+str(type(coop_wrapper)))
	highest_block_counter = coop_wrapper.count_num_longest_chains()
	num_counter = {}
	for key in highest_block_counter.keys():
		try:
			num_counter[highest_block_counter[key]] += 1
		except KeyError:
			num_counter[highest_block_counter[key]] = 1

	# Normalize hist values
	tot_count = 0
	for key in num_counter.keys():
		tot_count += num_counter[key]
	for key in num_counter.keys():
		num_counter[key] /= tot_count
	return num_counter

def heatmap_from_hists(list_of_dicts, array_of_times=None, cm_name="hot", ax=None):
	if not isinstance(list_of_dicts, list):
		raise TypeError("list_of_dicts should be of type list; currently of type"+str(type(list_of_dicts)))
	if not all(isinstance(item, dict) for item in list_of_dicts):
		raise TypeError("All items in list_of_dicts should be of type dict.")

	if array_of_times is not None:
		if not isinstance(array_of_times, np.ndarray):
			raise TypeError("array_of_times should be of type np.array; currently of type "+str(type(array_of_times)))
		assert len(list_of_dicts) == len(array_of_times), "list_of_dicts and array_of_times must be of equal length"
	else:
		array_of_times = np.array(list(range(len(list_of_dicts))))

	# Adapted from Yann's answer to the following StackOverflow post:
	# https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
	cm = plt.get_cmap(cm_name)
	cNorm = colors.Normalize(vmin=0, vmax=1)
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

	# Make dat plot!!!
	show_fig = False
	if not ax:
		show_fig = True
		fig = plt.figure()
		ax = fig.add_subplot(111)
	for time, book in zip(array_of_times, list_of_dicts):
		for num in book.keys():
			ax.plot([time], [num], color=scalarMap.to_rgba(book[num]), marker=".")
	ax.set_xlabel("Timestep")
	ax.set_ylabel("Number of Nodes Adhering to Chain")
	ax.set_title("Relative Frequency of Different Chain-Adherences")

	if show_fig:
		plt.show()

def global_chain_adherence_graph(list_of_nodes, dir_name):
	"""
	From a set of node instances from the same cooperative_wrapper,
	create the union of all local blockchains. From here, show for each node
	which subset of this union they adhere to. Meant to motivate local forking
	of blockchains
	"""
	# Assert trivial type-conformity
	if not isinstance(list_of_nodes, list):
		raise TypeError("list_of_nodes should be of type list; currently of type "+str(type(list_of_nodes)))
	if not all([isinstance(node, cooperative_node) for node in list_of_nodes]):
		raise TypeError("All items in list_of_nodes should be of type cooperative_node.")
	if not isinstance(dir_name, str):
		raise TypeError("dir_name should be of type str; currently of type "+str(type(dir_name)))

	# Assert that all nodes share same cooperative_wrapper
	if not all([node.universe == list_of_nodes[0].universe for node in list_of_nodes]):
		raise ValueError("All nodes in list_of_nodes should share the same universe attribute.")

	# Get list of quasi_roots from these cooperative_node instances
	quasi_roots = [node.get_root_block() for node in list_of_nodes]

	# Get union of local chains
	union_root = union_of_local_chains(quasi_roots)

	for j, quasi_root in enumerate([union_root]+quasi_roots):
		visualize_subtree(quasi_root, filename=dir_name+"_"+str(j))
