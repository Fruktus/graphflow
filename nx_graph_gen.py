# pylint: skip-file
import gzip
import re
import sys

import networkx as nx
from operator import itemgetter
import random
random.seed('asdasd')

size = 200
G = nx.random_geometric_graph(size, 0.125)
nx.set_node_attributes(G, 0, name='infected')
nx.set_node_attributes(G, 0, name='recovered')
initial = {}
for _ in range(random.randint(5, 10)):
    initial = {random.randint(0, size): {'infected': 1}}

nx.set_node_attributes(G, initial)

nx.write_gml(G, "large_graph.gml")

####################################

G = nx.balanced_tree(3, 5)
nx.set_node_attributes(G, 0, name='infected')
nx.set_node_attributes(G, 0, name='recovered')
initial = {}
for _ in range(random.randint(5, 10)):
    initial = {random.randint(0, len(list(G.nodes()))): {'infected': 1}}

nx.set_node_attributes(G, initial)
nx.write_gml(G, "tree_graph.gml")

##############################3

n = 1000
m = 2
G = nx.generators.barabasi_albert_graph(n, m)
# find node with largest degree
node_and_degree = G.degree()
(largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
# Create ego graph of main hub
hub_ego = nx.ego_graph(G, largest_hub)
nx.set_node_attributes(G, 0, name='infected')
nx.set_node_attributes(G, 0, name='recovered')
initial = {}
for _ in range(random.randint(5, 10)):
    initial = {random.randint(0, len(list(G.nodes()))): {'infected': 1}}

nx.set_node_attributes(G, initial)
nx.write_gml(G, "ego_graph.gml")

##############################

G = nx.Graph()
try:
    fh = open('lanl_routes.edgelist', 'r')
except IOError:
    print("lanl.edges not found")
    raise

time = {0: 0}
for line in fh.readlines():
    (head, tail, rtt) = line.split()
    G.add_edge(int(head), int(tail))
    time[int(head)] = float(rtt)

# get largest component and assign ping times to G0time dictionary
G0 = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
G0.rtt = {}
for n in G0:
    G0.rtt[n] = time[n]

nx.set_node_attributes(G, 0, name='infected')
nx.set_node_attributes(G, 0, name='recovered')
initial = {}
for _ in range(random.randint(5, 10)):
    initial = {random.randint(0, len(list(G.nodes()))): {'infected': 1}}

nx.set_node_attributes(G, initial)
nx.write_gml(G, "lanl_graph.gml")

#####################################

fh = gzip.open('roget_dat.txt.gz', 'r')

G = nx.DiGraph()

for line in fh.readlines():
    line = line.decode()
    if line.startswith("*"):  # skip comments
        continue
    if line.startswith(" "):  # this is a continuation line, append
        line = oldline + line
    if line.endswith("\\\n"):  # continuation line, buffer, goto next
        oldline = line.strip("\\\n")
        continue

    (headname, tails) = line.split(":")

    # head
    numfind = re.compile("^\d+")  # re to find the number of this word
    head = numfind.findall(headname)[0]  # get the number

    G.add_node(head)

    for tail in tails.split():
        if head == tail:
            print("skipping self loop", head, tail, file=sys.stderr)
        G.add_edge(head, tail)

nx.set_node_attributes(G, 0, name='infected')
nx.set_node_attributes(G, 0, name='recovered')
initial = {}
for _ in range(random.randint(5, 10)):
    initial = {random.randint(0, len(list(G.nodes()))): {'infected': 1}}

nx.set_node_attributes(G, initial)
nx.write_gml(G, "roget_graph.gml")

