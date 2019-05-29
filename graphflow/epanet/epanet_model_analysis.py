import networkx as nx

from graphflow.epanet.epanet_model import EpanetFlowNetwork

# general metrics
def degree_centrality(network: EpanetFlowNetwork):
    return nx.degree_centrality(network.get_networkx_graph())


def hits(network: EpanetFlowNetwork):
    return nx.hits_scipy(network.get_networkx_graph())


def diameter(network: EpanetFlowNetwork):
    return nx.algorithms.distance_measures.diameter(network.get_networkx_graph())


def degree(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.degree_centrality(network.get_networkx_graph())


def density(network: EpanetFlowNetwork):
    raw_network = network.get_networkx_graph()
    e = len(raw_network.edges)
    v = len(raw_network.nodes)
    return e/(v*(v-1))


def modularity(network: EpanetFlowNetwork):
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(network.get_networkx_graph())


def page_rank(network: EpanetFlowNetwork):
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(network.get_networkx_graph())


def hits(network: EpanetFlowNetwork):
    return nx.algorithms.link_analysis.hits_alg.hits(network.get_networkx_graph())


def eigenvector_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.eigenvector_centrality(network.get_networkx_graph())


def hits(network: EpanetFlowNetwork):
    return nx.algorithms.link_analysis.hits_alg.hits(network.get_networkx_graph())


def closeness_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.closeness_centrality(network.get_networkx_graph())


def betweenness_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.betweenness_centrality(network.get_networkx_graph())


def average_path(network: EpanetFlowNetwork):
    try:
        return nx.algorithms.shortest_paths.generic.average_shortest_path_length(network.get_networkx_graph())
    except Exception:
        return 0


# specific metrics
def maximum_flow(network: EpanetFlowNetwork, source, target):
    # TODO add util for finding source/target?
    try:
        return nx.algorithms.flow.maximum_flow_value(network.get_networkx_graph(), source, target)
    except Exception:
        return 0.0


def current_flow_closeness(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.current_flow_closeness_centrality(network.get_networkx_graph())


def current_flow_betweenness(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.current_flow_betweenness_centrality(network.get_networkx_graph())


def load_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.load_centrality(network.get_networkx_graph())


def subgraph(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.subgraph_centrality(network.get_networkx_graph())


def harmonic_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.harmonic_centrality(network.get_networkx_graph())


def global_reaching(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.global_reaching_centrality(network.get_networkx_graph())


def percolation(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.percolation_centrality(network.get_networkx_graph())


def second_order_centrality(network: EpanetFlowNetwork):
    return nx.algorithms.centrality.second_order_centrality(network.get_networkx_graph())
