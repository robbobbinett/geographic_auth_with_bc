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
from figure_props import heatmap_from_hists

cwd = getcwd()
# Only look at chain_hist pickles
onlyfiles = [f for f in listdir(cwd+"/pickle_dir/") if "chain_hist" in f]
for f in tqdm(onlyfiles):
	param_str = f.replace("_chain_hist.pkl", "")
	with open("pickle_dir/"+f, "rb") as file:
		hists = load(file)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	heatmap_from_hists(hists, ax=ax)
	fig.savefig("analysis/"+param_str+".pdf")
	plt.close("all")
