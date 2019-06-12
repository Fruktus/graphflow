import random
import networkx as nx
import sys

# get raw networkx graph and generates 'infected' and 'recovered' labels values for each node with given probability
# input can be: samples/raw_graph_sample 0.2 0.1

input_name = sys.argv[1]
G = nx.read_gml(input_name)

infected_prob = float(sys.argv[2])
recovered_prob = float(sys.argv[3])

for n in nx.nodes(G):

    recovered = False
    infected = False
    val = random.random()

    if val < infected_prob:
        infected = True
    elif val < infected_prob + recovered_prob:
        recovered = True

    attrs = {n: {'infected': infected, 'recovered': recovered}}
    nx.set_node_attributes(G, attrs)

nx.write_gml(G, input_name + "_out")
