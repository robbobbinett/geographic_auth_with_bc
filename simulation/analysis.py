# The block below is due to pycraft on StackOverflow:
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
# Following code is adapted from his answer
###
from os import listdir, getcwd
from os.path import isfile, join
###
from pickle import load
import matplotlib.pyplot as plt
from tqdm import tqdm
from figure_props import heatmap_from_hists, connected_components_over_time

cwd = getcwd()
# Only look at chain_hist pickles
if False:
	onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if ("chain_hist" in f) and ("longest" not in f)]
	print("Doing chain_hist graphics...")
	for f in tqdm(onlyfiles):
		param_str = f.replace("_chain_hist.pkl", "")
		with open("pickle_dir/"+f, "rb") as file:
			hists = load(file)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		heatmap_from_hists(hists, ax=ax)
		ax.set_title(param_str)
		fig.savefig("analysis/chain_hist/"+param_str+".pdf")
		plt.close("all")

# Only look at adj_mat pickles
if True:
	print("Doing adj_mat graphics...")
	onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "adj_mat" in f]
	for f in tqdm(onlyfiles):
		param_str = f.replace("_adj_mat.pkl", "")
		param_list = param_str.split("_")
		num_nodes = int(param_list[0])
		cycle_rat = int(param_list[-1])
		with open ("pickle_dir/"+f, "rb") as file:
			adj_mats = load(file)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		connected_components_over_time(adj_mats, ax=ax)
		ax.set_title("SPAN Connected Components over Time:\n"+str(num_nodes)+" Nodes,\n"+str(cycle_rat)+" Message Cycles per SPAN Cycle")
		ax.set_xlabel("# SPAN Cycles")
		ax.set_ylabel("# Connected Components")
		fig.savefig("analysis/adj_mat/"+param_str+".pdf")
		plt.close("all")

# Only look at longest_chain_hist pickles
if True:
	onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "longest_chain_hist" in f]
	print("Doing longest_chain_hist graphics...")
	for f in tqdm(onlyfiles):
		param_str = f.replace("_longest_chain_hist.pkl", "")
		param_list = param_str.split("_")
		num_nodes = int(param_list[0])
		cycle_rat = int(param_list[-1])
		with open("pickle_dir/"+f, "rb") as file:
			hists = load(file)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		heatmap_from_hists(hists, ax=ax)
		ax.set_title("Longest Chains over Time:\n"+str(num_nodes)+" Nodes,\n"+str(cycle_rat)+" Message Cycles per Message-Passing Cycle")
		ax.set_xlabel("# Message-Passing Cycles")
		ax.set_ylabel("# Nodes Recognizing Chain")
		fig.savefig("analysis/longest_chain_hist/"+param_str+".pdf")
		plt.close("all")

# Only look at leaf pickles
if False:
	onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "leaf" in f]
	print("Doing leaf graphics...")
	for f in tqdm(onlyfiles):
		param_str = f.replace("_leaf.pkl", "")
		with open("pickle_dir/"+f, "rb") as file:
			hists = load(file)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		heatmap_from_hists(hists, ax=ax)
		ax.set_title(param_str)
		fig.savefig("analysis/leaf/"+param_str+".pdf")
		plt.close("all")
