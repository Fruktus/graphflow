import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network_from_network


def degree_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.degree_centrality(raw_network)


def hits(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.hits_scipy(raw_network)
