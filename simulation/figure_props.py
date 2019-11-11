from block_props import fixed_block

def visualize_subtree(quasi_root):
	if not isinstance(quasi_root, fixed_block):
		raise TypeError("quasi_root should be of type fixed_block; currently of type "+str(type(fixed_block)))

	# Get BFS ordering of blocks by height
	blocks_by_height = quasi_root.return_bfs()
	print(blocks_by_height)

	# Get dictionary storing blocks by given height
	height_collection = {}
	for block in blocks_by_height:
		try:
			height_collection[block.height].append(block)
		except KeyError:
			height_collection[block.height] = []

	# Count number of blocks of given height
	heights = list(height_collection.keys())
	heights.sort()
	height_dict = dict((key, len(height_collection[key])) for key in heights)

	# Create graphviz nodes for all blocks, starting from quasi_root
	replace1 = ""
	for height in heights:
		width = height_dict[height]
		for j, block in zip(range(width), height_collection[height]):
			replace1 += str(block.block.id)+' [pos="'+str((j+1)/width)+','+str(-height)+"!"+'];\n'

	# Draw edges from parents to children
	for block in blocks_by_height:
		for child in block.children:
			replace1 += str(block.block.id) + " -> " + str(child.block.id) + ";\n"

	# Export .dot file
	with open("figure_templates/local_chain_template.txt", "r") as base_file:
		with open ("figure_intermediates/local_chains/"+str(quasi_root.block.id)+".dot", "w") as new_file:
			new_file.write(base_file.read().replace('//replace', replace1))
