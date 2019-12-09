import random
from itertools import product
from simulation_props import standard_routine
from message_props import BestowBlockTimeoutError
from coop_tor_node import make_coop_tor_wrapper

sizes = [10, 30, 50, 100]
rs = [0.05, 0.1, 0.25, 0.5]
ss = [0.05, 0.1, 0.15, 0.2]

for size, r, s in product(sizes, rs, ss):
	chance_the = make_coop_tor_wrapper(size, r, s, random.random)
	try:
		standard_routine(chance_the, 10, 5)
	except BestowBlockTimeoutError:
		print("The following parameter combos led to bestow_block_timeout:")
		print("size: "+str(size))
		print("r: "+str(r))
		print("s: "+str(s))
