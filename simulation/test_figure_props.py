from figure_props import *
from block_props import *
import matplotlib.pyplot as plt

"""
Test that the fixed_block primitive creates trees in the expected
fashion; tested using toy tree examples.
"""
# The one-node rooted tree
root = fixed_block(null_block)

# The ten-node (rooted) path
prev_free_block = null_block
prev_fixed_block = root
fixed_block_book = {0: prev_fixed_block}
for j in range(1, 10):
	curr_fixed_block = prev_fixed_block.add_child(free_block(j, prev_free_block))
	prev_fixed_block = curr_fixed_block
	prev_free_block = curr_fixed_block.block
	fixed_block_book[j] = prev_fixed_block

# The following rooted tree
#
# o  o
# | /
# o  o
# | /
# o
# |
# o
# |
# oo
# |   /
# o  o
# | /
# o
# |
# o  o
# | /
# o  o
# | /
# o
# 
# NOTE: As the original nodes have IDs 0-9, these new nodes will
# be labeled 10-15, from smallest-to-highest height.
fixed_block_book[10] = root.add_child(free_block(10, null_block))
fixed_block_book[11] = fixed_block_book[1].add_child(free_block(11, fixed_block_book[1].block))
fixed_block_book[12] = fixed_block_book[3].add_child(free_block(12, fixed_block_book[3].block))
fixed_block_book[13] = fixed_block_book[12].add_child(free_block(13, fixed_block_book[12].block))
fixed_block_book[14] = fixed_block_book[7].add_child(free_block(14, fixed_block_book[7].block))
fixed_block_book[15] = fixed_block_book[8].add_child(free_block(15, fixed_block_book[8].block))

visualize_subtree(root)
