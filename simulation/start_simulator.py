import simpy
from node_props import make_universe_of_nodes

env = simpy.Environment()
universe = make_universe_of_nodes(1000)
print(universe)
