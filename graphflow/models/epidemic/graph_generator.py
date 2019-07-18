import sys
import random
import networkx as nx

# get raw networkx graph and generates 'infected' and 'recovered' labels values for each node with given probability
# input can be: samples/raw_graph_sample.gml 0.2 0.1

INPUT_NAME = sys.argv[1]
G = nx.read_gml(INPUT_NAME)

INFECTED_PROB = float(sys.argv[2])
RECOVERED_PROB = float(sys.argv[3])

for n in nx.nodes(G):

    recovered = False
    infected = False
    val = random.random()

    if val < INFECTED_PROB:
        infected = True
    elif val < INFECTED_PROB + RECOVERED_PROB:
        recovered = True

    attrs = {n: {'infected': infected, 'recovered': recovered}}
    nx.set_node_attributes(G, attrs)

nx.write_gml(G, INPUT_NAME + "_out")
