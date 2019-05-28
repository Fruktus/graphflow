import networkx as nx

from graphflow.epanet.epanet_model import EpanetFlowNetwork


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

