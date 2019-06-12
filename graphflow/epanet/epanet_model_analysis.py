import networkx as nx

from graphflow.epanet.epanet_model import EpanetFlowNetwork


# general metrics
def degree_centrality(network: EpanetFlowNetwork):
    return nx.degree_centrality(network.get_networkx_graph())


def hits(network: EpanetFlowNetwork):
    try:
        return nx.hits_scipy(network.get_networkx_graph(), max_iter=10000)
    except nx.PowerIterationFailedConvergence:
        return None


def diameter(network: EpanetFlowNetwork):
    try:
        return nx.algorithms.distance_measures.diameter(network.get_networkx_graph())
    except nx.NetworkXError:
        return 0


def degree(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.degree_centrality(network.get_networkx_graph())


def density(network: EpanetFlowNetwork):
    raw_network = network.get_networkx_graph()
    edges = len(raw_network.edges)
    vertices = len(raw_network.nodes)
    return edges/(vertices*(vertices-1))


def modularity(network: EpanetFlowNetwork):
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(network.get_networkx_graph())


def page_rank(network: EpanetFlowNetwork):
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(nx.Graph(network.get_networkx_graph()))


def eigenvector_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.eigenvector_centrality(nx.Graph(network.get_networkx_graph()), max_iter=10000)


def closeness_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.closeness_centrality(network.get_networkx_graph())


def betweenness_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.betweenness_centrality(network.get_networkx_graph())


def average_path(network: EpanetFlowNetwork):
    return nx.algorithms.shortest_paths.generic.average_shortest_path_length(network.get_networkx_graph())


# specific metrics
def maximum_flow(network: EpanetFlowNetwork, source, target):
    try:
        return nx.algorithms.flow.maximum_flow_value(network.get_networkx_graph(), source, target)
    except nx.NetworkXError:
        return 0.0
    except nx.NetworkXUnbounded:
        return 0.0


def current_flow_closeness(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.current_flow_closeness_centrality(network.get_networkx_graph().to_undirected())


def current_flow_betweenness(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.current_flow_betweenness_centrality(network.get_networkx_graph().to_undirected())


def load_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.load_centrality(network.get_networkx_graph())


def subgraph(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.subgraph_centrality(nx.Graph(network.get_networkx_graph().to_undirected()))


def harmonic_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.harmonic_centrality(network.get_networkx_graph())


def global_reaching(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.global_reaching_centrality(network.get_networkx_graph())


def percolation(network: EpanetFlowNetwork):
    try:
        return nx.algorithms.centrality.percolation_centrality(network.get_networkx_graph())
    except KeyError:
        return {}


def second_order_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.second_order_centrality(nx.Graph(network.get_networkx_graph()).to_undirected())
