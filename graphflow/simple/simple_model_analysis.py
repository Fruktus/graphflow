import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network_from_network

# general metrics
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


# specific metrics
def maximum_flow(network: SimpleFlowNetwork, source, target):
    # TODO add util for finding source/target?
    raw_network = __build_raw_network_from_network(network)
    try:
        return nx.algorithms.flow.maximum_flow_value(raw_network, source, target)
    except Exception:
        return 0.0


def current_flow_closeness(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.current_flow_closeness_centrality(raw_network)


def current_flow_betweenness(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.current_flow_betweenness_centrality(raw_network)


def load_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.load_centrality(raw_network)


def subgraph(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.subgraph_centrality(raw_network)


def harmonic_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.harmonic_centrality(raw_network)


def global_reaching(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.global_reaching_centrality(raw_network)


def percolation(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.percolation_centrality(raw_network)


def second_order_centrality(network: SimpleFlowNetwork):
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.second_order_centrality(raw_network)
