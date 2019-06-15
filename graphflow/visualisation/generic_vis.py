# pylint: disable=E1101

import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import networkx as nx

from graphflow.analysis.network_utils import get_nx_network


def visualize_holoviews(network, metrics: [tuple] = None):
    """metrics is an array of two-tuple consisting of string (metric name) and dict or value returned from metric"""
    hv.extension('bokeh')

    nx_network = get_nx_network(network)
    if metrics:
        for i in metrics:
            if isinstance(i[1], dict):
                nx.set_node_attributes(nx_network, i[1], i[0])
            else:
                print(i[0], ":", i[1])

    defaults = dict(width=700, height=700, padding=0.1)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
    network_graph = hv.Graph.from_networkx(
        nx_network, nx.layout.spring_layout).opts(tools=['hover'], directed=True, arrowhead_length=0.05)

    renderer = hv.renderer('bokeh')
    plot = renderer.get_plot(network_graph).state
    output_file("graph.html")
    show(plot)

