import networkx as nx

from graphflow.analysis.network_utils import get_nx_network


def calculate_metric(ntype, name, network):
    """calls available metrics (those in this document)
       returns results (mostly dicts and numerical values"""
    try:
        if ntype == 'simple':
            return name, globals()[name](network)
        if ntype == 'extended':
            return name, globals()[name](network)
        if ntype == 'epanet':
            return name, globals()[name](network)
        if ntype == 'epidemic':
            return name, globals()[name](network)
        raise TypeError('unknown network type')
    except KeyError:
        print('unknown key: ', name)
        return None


def calculate_metric_array(ntype: str, network, array: [str]):
    """same as calculate_metric, but processes an array instead of a single metric.
       returns an array containing the results (dicts or values)"""
    arr = []
    for i in array:
        res = calculate_metric(ntype, i, network)
        if res:
            arr.append(res)
    return arr


# general metrics
def degree_centrality(network):
    """returns: Dictionary of nodes with degree centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.degree_centrality(nxnetwork)


def hits(network):
    """"Returns: (hubs,authorities) – Two dictionaries keyed by node containing the hub and authority values."""
    try:
        nxnetwork = get_nx_network(network)
        return nx.hits_scipy(nxnetwork)
    except nx.PowerIterationFailedConvergence:
        return None


def diameter(network):
    """Returns:	d (Integer) – Diameter of graph"""
    try:
        nxnetwork = get_nx_network(network)
        return nx.algorithms.distance_measures.diameter(nxnetwork)
    except nx.NetworkXError:
        return 0


def density(network):
    """Returns: density (Float)"""
    nxnetwork = get_nx_network(network)
    edges = len(nxnetwork.edges)
    vertices = len(nxnetwork.nodes)
    return edges / (vertices * (vertices - 1))


def modularity(network):
    """Returns: None, Yields sets of nodes, one for each community."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(nxnetwork)


def page_rank(network):
    """Returns:	pagerank – Dictionary of nodes with PageRank as value"""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(nxnetwork)


def eigenvector_centrality(network):
    """Returns:	nodes – Dictionary of nodes with eigenvector centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.eigenvector_centrality(nxnetwork, max_iter=1000)


def closeness_centrality(network):
    """Returns:	nodes – Dictionary of nodes with closeness centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.closeness_centrality(nxnetwork)


def betweenness_centrality(network):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.betweenness_centrality(nxnetwork)


def average_path(network):
    """Returns: average shortest path length."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.shortest_paths.generic.average_shortest_path_length(nxnetwork)


# specific metrics
def maximum_flow(network, source, target):
    """flow_value (integer, float) – Value of the maximum flow, i.e., net outflow from the source.
       flow_dict (dict) – A dictionary containing the value of the flow that went through each edge."""
    nxnetwork = get_nx_network(network)
    try:
        return nx.algorithms.flow.maximum_flow_value(nxnetwork, source, target)
    except nx.NetworkXError:
        return 0.0
    except nx.NetworkXUnbounded:
        return 0.0


def current_flow_closeness(network):
    """Returns:	nodes – Dictionary of nodes with current flow closeness centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.current_flow_closeness_centrality(nxnetwork.to_undirected())


def current_flow_betweenness(network):
    """Returns:	nodes – Dictionary of nodes with betweenness centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.current_flow_betweenness_centrality(nxnetwork.to_undirected())


def load_centrality(network):
    """Returns:	nodes – Dictionary of nodes with centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.load_centrality(nxnetwork)


def subgraph(network):
    """Returns:	nodes – Dictionary of nodes with subgraph centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.subgraph_centrality(nxnetwork.to_undirected())


def harmonic_centrality(network):
    """Returns:	nodes – Dictionary of nodes with harmonic centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.harmonic_centrality(nxnetwork)


def global_reaching(network):
    """Returns:	h (Float) – The global reaching centrality of the graph."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.global_reaching_centrality(nxnetwork)


def percolation(network):
    """Returns:	nodes – Dictionary of nodes with percolation centrality as the value."""
    try:
        nxnetwork = get_nx_network(network)
        return nx.algorithms.centrality.percolation_centrality(nxnetwork)
    except KeyError:
        return {}


def second_order_centrality(network):
    """Returns:	nodes – Dictionary keyed by node with second order centrality as the value."""
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.second_order_centrality(nxnetwork.to_undirected())
