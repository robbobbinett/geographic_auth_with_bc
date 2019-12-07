# The block below is due to pycraft on StackOverflow:
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
# Following code is adapted from his answer
###
from os import listdir, getcwd
from os.path import isfile, join
###

cwd = getcwd()
onlyfiles = [f for f in listdir(cwd+"/figure_intermediates/local_chains/") if "small_world" not in f]
to_append = [f for f in listdir(cwd+"/figure_intermediates/local_chains/small_world/")]
onlyfiles += ["small_world/"+name for name in to_append]
number_strings = [f.replace(cwd+"/figure_intermediates/local_chains/", "").replace(".dot", "") for f in onlyfiles]
print(" ".join(number_strings))
