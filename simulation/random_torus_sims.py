import random
from itertools import product
from pickle import dump
from simulation_props import standard_routine
from message_props import BestowBlockTimeoutError
from coop_tor_node import make_coop_tor_wrapper

sizes = [10, 30, 50, 100]
rs = [0.05, 0.1, 0.25, 0.5]
ss = [0.05, 0.1, 0.15, 0.2]
rel_update_freqs = [3, 5, 10]
sim_length = 100
pickling = True

for size, r, s, ruf in product(sizes, rs, ss, rel_update_freqs):
	chain_hist_store = []
	leaf_hist_store = []
	adj_mat_store = []
	chance_the = make_coop_tor_wrapper(size, r, s, random.random)
	standard_routine(chance_the, sim_length, ruf, forgive_timeout=True, chain_hist_store=chain_hist_store, leaf_hist_store=leaf_hist_store, adj_mat_store=adj_mat_store)
	if pickling:
		file_prefix = "_".join(str(elem) for elem in [size, r, s, ruf])
		with open("pickle_dir/"+file_prefix+"_chain_hist.pkl", "wb") as f:
			dump(chain_hist_store, f)
		with open("pickle_dir/"+file_prefix+"_leaf.pkl", "wb") as f:
			dump(leaf_hist_store, f)
		with open("pickle_dir/"+file_prefix+"_adj_mat.pkl", "wb") as f:
			dump(adj_mat_store, f)
