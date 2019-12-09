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
print("Doing adj_mat graphics...")
onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "adj_mat" in f]
for f in tqdm(onlyfiles):
	param_str = f.replace("_adj_mat.pkl", "")
	with open ("pickle_dir/"+f, "rb") as file:
		adj_mats = load(file)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	connected_components_over_time(adj_mats, ax=ax)
	ax.set_title(param_str)
	fig.savefig("analysis/adj_mat/"+param_str+".pdf")
	plt.close("all")

# Only look at longest_chain_hist pickles
onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "longest_chain_hist" in f]
print("Doing longest_chain_hist graphics...")
for f in tqdm(onlyfiles):
	param_str = f.replace("_longest_chain_hist.pkl", "")
	with open("pickle_dir/"+f, "rb") as file:
		hists = load(file)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	heatmap_from_hists(hists, ax=ax)
	ax.set_title(param_str)
	fig.savefig("analysis/longest_chain_hist/"+param_str+".pdf")
	plt.close("all")
