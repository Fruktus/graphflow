# pylint: disable=E1101

import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import matplotlib.pyplot as plt
import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_raw_network
from graphflow.simple.simple_model_utils import __build_string_network


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


def visualize_holoviews(network: SimpleFlowNetwork, metrics: [tuple] = None):
    """metrics is an array of two-tuple consisting of string (metric name) and dict or value returned from metric"""
    nodes, edges = network.get_network_state()
    hv.extension('bokeh')

    string_network = __build_string_network(nodes, edges)
    if metrics:
        for i in metrics:
            if isinstance(i[1], dict):
                nx.set_node_attributes(string_network, i[1], i[0])
            else:
                print(i[0], ":", i[1])

    defaults = dict(width=700, height=700, padding=0.1)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
    network_graph = hv.Graph.from_networkx(
        string_network, nx.layout.spring_layout).opts(tools=['hover'], directed=True, arrowhead_length=0.05)

    renderer = hv.renderer('bokeh')
    plot = renderer.get_plot(network_graph).state
    output_file("graph.html")
    show(plot)
