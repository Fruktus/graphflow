import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network_from_network


def degree_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.degree_centrality(raw_network)


def hits(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.hits_scipy(raw_network)


def diameter(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.distance_measures.diameter(raw_network)


def degree(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.degree_centrality(raw_network)


def density(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    e = len(raw_network.edges)
    v = len(raw_network.nodes)
    return e/(v*(v-1))


def modularity(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(raw_network)


def page_rank(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(raw_network)


def hits(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.link_analysis.hits_alg.hits(raw_network)


def eigenvector_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.eigenvector_centrality(raw_network)


def hits(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.link_analysis.hits_alg.hits(raw_network)


def closeness_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.closeness_centrality(raw_network)


def betweenness_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.betweenness_centrality(raw_network)


def average_path(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    try:
        return nx.algorithms.shortest_paths.generic.average_shortest_path_length(raw_network)
    except Exception:
        return 0

