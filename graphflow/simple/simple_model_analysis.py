import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network_from_network


def degree_centrality(network: SimpleFlowNetwork):
    """returns: Dictionary of nodes with degree centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.degree_centrality(raw_network)


def hits(network: SimpleFlowNetwork):
    """"Returns: (hubs,authorities) – Two dictionaries keyed by node containing the hub and authority values."""
    try:
        raw_network = __build_raw_network_from_network(network)
        return nx.hits_scipy(raw_network)
    except Exception:
        return None


def diameter(network: SimpleFlowNetwork):
    """Returns:	d (Integer) – Diameter of graph"""
    try:
        raw_network = __build_raw_network_from_network(network)
        return nx.algorithms.distance_measures.diameter(raw_network)
    except Exception:
        return 0


def density(network: SimpleFlowNetwork):
    """Returns: density (Float)"""
    raw_network = __build_raw_network_from_network(network)
    e = len(raw_network.edges)
    v = len(raw_network.nodes)
    return e/(v*(v-1))


def modularity(network: SimpleFlowNetwork):
    """Returns: None, Yields sets of nodes, one for each community."""
    try:
        raw_network = __build_raw_network_from_network(network)
        return nx.algorithms.community.modularity_max.greedy_modularity_communities(raw_network)
    except Exception:
        return None


def page_rank(network: SimpleFlowNetwork):
    """Returns:	pagerank – Dictionary of nodes with PageRank as value"""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(raw_network)


def eigenvector_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with eigenvector centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.eigenvector_centrality(raw_network, max_iter=1000)


def closeness_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with closeness centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.closeness_centrality(raw_network)


def betweenness_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.betweenness_centrality(raw_network)


def average_path(network: SimpleFlowNetwork):
    """Returns: average shortest path length."""
    raw_network = __build_raw_network_from_network(network)
    try:
        return nx.algorithms.shortest_paths.generic.average_shortest_path_length(raw_network)
    except Exception:
        return 0


# specific metrics
def maximum_flow(network: SimpleFlowNetwork, source, target):
    """flow_value (integer, float) – Value of the maximum flow, i.e., net outflow from the source.
       flow_dict (dict) – A dictionary containing the value of the flow that went through each edge."""
    # TODO add util for finding source/target?
    raw_network = __build_raw_network_from_network(network)
    try:
        return nx.algorithms.flow.maximum_flow_value(raw_network, source, target)
    except Exception:
        return 0.0


def current_flow_closeness(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with current flow closeness centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.current_flow_closeness_centrality(raw_network.to_undirected())


def current_flow_betweenness(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.current_flow_betweenness_centrality(raw_network.to_undirected())


def load_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.load_centrality(raw_network)


def subgraph(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with subgraph centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.subgraph_centrality(raw_network.to_undirected())


def harmonic_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with harmonic centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.harmonic_centrality(raw_network)


def global_reaching(network: SimpleFlowNetwork):
    """Returns:	h (Float) – The global reaching centrality of the graph."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.global_reaching_centrality(raw_network)


def percolation(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary of nodes with percolation centrality as the value."""
    try:
        raw_network = __build_raw_network_from_network(network)
        return nx.algorithms.centrality.percolation_centrality(raw_network)
    except Exception:
        return {}


def second_order_centrality(network: SimpleFlowNetwork):
    """Returns:	nodes – Dictionary keyed by node with second order centrality as the value."""
    raw_network = __build_raw_network_from_network(network)
    return nx.algorithms.centrality.second_order_centrality(raw_network.to_undirected())
