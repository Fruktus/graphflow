"""
General metrics

This file contains general metrics which are available for all models.

The following describes all metrics not only general.

Metric is recognised by functions name. Names have to start
with either ``static_`` or ``dynamic_`` after which is metric name in snake_case. The first word states if the metric
is static - can be calculated only once, or dynamic - depends on graphs state and has to be calculated for each time
step. The graphs themselves are not dynamic meaning that they can't remove/add nodes and edges during simulation but
their state - nodes attributes mostly can change. Thus dynamic metrics.

Each metric is function with similar pattern:

Args:
    network (graph): NetworkX graph on which metric will be calculated

Returns:
    One of the following (depending on metric):
        int or float: Metric represents entire network (graph) property. Eg diameter
        dict: Dictionary (node: value). Represents nodes properties.
        tuple: (dict, dict). Similar to previous but returns two values
"""

import networkx as nx


# general metrics
def static_degree_centrality(network):
    """returns: Dictionary of nodes with degree centrality as the value."""
    return nx.degree_centrality(network)


def hits(network):
    """"Returns: (hubs,authorities) – Two dictionaries keyed by node containing the hub and authority values."""
    try:
        return nx.hits_scipy(network)
    except nx.PowerIterationFailedConvergence:
        return None


def diameter(network):
    """Returns:	d (Integer) – Diameter of graph"""
    try:
        return nx.algorithms.distance_measures.diameter(network)
    except nx.NetworkXError:
        return 0


def density(network):
    """Returns: density (Float)"""
    edges = len(network.edges)
    vertices = len(network.nodes)
    return edges / (vertices * (vertices - 1))


# TODO This one works weird. It has to be either changed or removed
def modularity(network):
    """Returns: None, Yields sets of nodes, one for each community."""
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(network)


def page_rank(network):
    """Returns:	pagerank – Dictionary of nodes with PageRank as value"""
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(network)


def eigenvector_centrality(network):
    """Returns:	nodes – Dictionary of nodes with eigenvector centrality as the value."""
    return nx.algorithms.centrality.eigenvector_centrality(network, max_iter=1000)


def closeness_centrality(network):
    """Returns:	nodes – Dictionary of nodes with closeness centrality as the value."""
    return nx.algorithms.centrality.closeness_centrality(network)


def betweenness_centrality(network):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    return nx.algorithms.centrality.betweenness_centrality(network)


def average_path(network):
    """Returns: average shortest path length."""
    return nx.algorithms.shortest_paths.generic.average_shortest_path_length(network)


# specific metrics
def maximum_flow(network, source, target):
    """flow_value (integer, float) – Value of the maximum flow, i.e., net outflow from the source.
       flow_dict (dict) – A dictionary containing the value of the flow that went through each edge."""
    try:
        return nx.algorithms.flow.maximum_flow_value(network, source, target)
    except nx.NetworkXError:
        return 0.0
    except nx.NetworkXUnbounded:
        return 0.0


def current_flow_closeness(network):
    """Returns:	nodes – Dictionary of nodes with current flow closeness centrality as the value."""
    return nx.algorithms.centrality.current_flow_closeness_centrality(network.to_undirected())


def current_flow_betweenness(network):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    return nx.algorithms.centrality.current_flow_betweenness_centrality(network.to_undirected())


def load_centrality(network):
    """Returns:	nodes – Dictionary of nodes with centrality as the value."""
    return nx.algorithms.centrality.load_centrality(network)


def subgraph(network):
    """Returns:	nodes – Dictionary of nodes with subgraph centrality as the value."""
    return nx.algorithms.centrality.subgraph_centrality(network.to_undirected())


def harmonic_centrality(network):
    """Returns:	nodes – Dictionary of nodes with harmonic centrality as the value."""
    return nx.algorithms.centrality.harmonic_centrality(network)


def global_reaching(network):
    """Returns:	h (Float) – The global reaching centrality of the graph."""
    return nx.algorithms.centrality.global_reaching_centrality(network)


def percolation(network):
    """Returns:	nodes – Dictionary of nodes with percolation centrality as the value."""
    try:
        return nx.algorithms.centrality.percolation_centrality(network)
    except KeyError:
        return {}


def second_order_centrality(network):
    """Returns:	nodes – Dictionary keyed by node with second order centrality as the value."""
    return nx.algorithms.centrality.second_order_centrality(network.to_undirected())
