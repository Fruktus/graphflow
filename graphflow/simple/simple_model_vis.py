# pylint: disable=E1101

import matplotlib.pyplot as plt
import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network


def visualize_matplotlib(network: SimpleFlowNetwork):
    nodes, edges = network.get_network_state()
    raw_network = __build_raw_network(nodes, edges)

    node_labels = {node[0]: node[1]['s_flow'] for node in raw_network.nodes(data=True)}
    edge_labels = {(edge[0], edge[1]): edge[2]['m_flow'] for edge in raw_network.edges(data=True)}

    graph_pos = nx.spring_layout(raw_network)
    nx.draw_networkx_nodes(raw_network, graph_pos, node_size=500)
    nx.draw_networkx_edges(raw_network, graph_pos, width=1.5)

    nx.draw_networkx_labels(raw_network, graph_pos, labels=node_labels, font_size=8)
    nx.draw_networkx_edge_labels(raw_network, graph_pos, edge_labels=edge_labels, font_size=8)
    plt.show()
