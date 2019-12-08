from itertools import product
from toroidal_node import *
from figure_props import *
from message_props import *

sizes = [10, 50, 100]
rs = [0.05, 0.1, 0.25, 0.5]
ss = [0.05, 0.1, 0.15, 0.2]

for size, r, s in product(sizes, rs, ss):
	torus = make_torus_of_nodes(size, r, s)
	chance_the = cooperative_wrapper(torus)
