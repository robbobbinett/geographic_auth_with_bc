# The block below is due to pycraft on StackOverflow:
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
# Following code is adapted from his answer
###
from os import listdir, getcwd
from os.path import isfile, join
###

cwd = getcwd()
onlyfiles = [f for f in listdir(cwd+"/figure_intermediates/local_chains/")]
number_strings = [f.replace(cwd+"/figure_intermediates/local_chains/", "").replace(".dot", "") for f in onlyfiles]
print(" ".join(number_strings))
