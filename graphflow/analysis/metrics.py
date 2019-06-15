import networkx as nx

from graphflow.analysis.network_utils import get_nx_network


def calculate_metric(ntype, name, network):
    try:
        if ntype == 'simple':
            return name, globals()[name](network)
        elif ntype == 'extended':
            return name, globals()[name](network)
        elif ntype == 'epanet':
            return name, globals()[name](network)
        elif ntype == 'epidemic':
            raise NotImplementedError('this feature was not yet implemented')
        else:
            raise TypeError('unknown network type')
    except KeyError:
        return


def calculate_metric_array(ntype: str, network, array: [str]):
    arr = []
    for i in array:
        arr.append((i, calculate_metric(ntype, i, network)))
    return arr

# general metrics
def degree_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.degree_centrality(nxnetwork)


def hits(network):
    try:
        nxnetwork = get_nx_network(network)
        return nx.hits_scipy(nxnetwork, max_iter=10000)
    except nx.PowerIterationFailedConvergence:
        return None


def diameter(network):
    try:
        nxnetwork = get_nx_network(network)
        return nx.algorithms.distance_measures.diameter(nxnetwork)
    except nx.NetworkXError:
        return 0


def degree(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.degree_centrality(nxnetwork)


def density(network):
    nxnetwork = get_nx_network(network)
    raw_network = nxnetwork
    edges = len(raw_network.edges)
    vertices = len(raw_network.nodes)
    return edges/(vertices*(vertices-1))


def modularity(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(nxnetwork)


def page_rank(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(nx.Graph(nxnetwork))


def eigenvector_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.eigenvector_centrality(nx.Graph(nxnetwork), max_iter=10000)


def closeness_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.closeness_centrality(nxnetwork)


def betweenness_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.betweenness_centrality(nxnetwork)


def average_path(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.shortest_paths.generic.average_shortest_path_length(nxnetwork)


# specific metrics
def maximum_flow(network, source, target):
    try:
        nxnetwork = get_nx_network(network)
        return nx.algorithms.flow.maximum_flow_value(nxnetwork, source, target)
    except nx.NetworkXError:
        return 0.0
    except nx.NetworkXUnbounded:
        return 0.0


def current_flow_closeness(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.current_flow_closeness_centrality(nxnetwork.to_undirected())


def current_flow_betweenness(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.current_flow_betweenness_centrality(nxnetwork.to_undirected())


def load_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.load_centrality(nxnetwork)


def subgraph(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.subgraph_centrality(nx.Graph(nxnetwork.to_undirected()))


def harmonic_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.harmonic_centrality(nxnetwork)


def global_reaching(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.global_reaching_centrality(nxnetwork)


def percolation(network):
    try:
        nxnetwork = get_nx_network(network)
        return nx.algorithms.centrality.percolation_centrality(nxnetwork)
    except KeyError:
        return {}


def second_order_centrality(network):
    nxnetwork = get_nx_network(network)
    return nx.algorithms.centrality.second_order_centrality(nx.Graph(nxnetwork).to_undirected())
