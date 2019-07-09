# pylint: disable=E1101
import webbrowser

import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import networkx as nx
import EoN

from graphflow.analysis.network_utils import get_nx_network


def visualize_holoviews(network, metrics: [tuple] = None):
    """metrics is an array of two-tuple consisting of string (metric name) and dict or value returned from metric"""
    hv.extension('bokeh')

    nx_network = get_nx_network(network)
    if metrics:
        for i in metrics:
            if isinstance(i[1], dict):
                nx.set_node_attributes(nx_network, i[1], i[0])
            elif isinstance(i[1], tuple):
                nx.set_node_attributes(nx_network, i[1][0], i[0])
            else:
                print(i[0], ":", i[1])

    defaults = dict(width=700, height=700, padding=0.1)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
    network_graph = hv.Graph.from_networkx(
        nx_network, nx.layout.spring_layout).opts(tools=['hover'], directed=True)

    renderer = hv.renderer('bokeh')
    plot = renderer.get_plot(network_graph).state
    output_file("graph.html")
    show(plot)


def visualize_epidemic(network, simulation_investigation: EoN.Simulation_Investigation,
                       metrics: [tuple] = None, max_time_steps=200):
    hv.extension('bokeh')

    nx_network = get_nx_network(network)

    for node in nx_network.nodes(data=True):
        del node[1]['infected']
        del node[1]['recovered']

    if simulation_investigation.SIR:
        time_steps = simulation_investigation.t()[1:]
    else:
        time_steps = simulation_investigation.t()[1:max_time_steps]

    layout = nx.layout.spring_layout(nx_network)
    graph_dict = {time: __get_epidemic_network_graph(nx_network, layout,
                                                     simulation_investigation.get_statuses(time=time),
                                                     metrics) for time in time_steps}
    hmap = hv.HoloMap(graph_dict, kdims='t')

    defaults = dict(width=700, height=700, padding=0.1)
    hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    filename = "graph.html"
    hv.save(hmap, filename, backend='bokeh')
    webbrowser.open(filename)


def __get_epidemic_network_graph(network, layout, statuses, metrics: [tuple] = None):
    if metrics:
        for i in metrics:
            if isinstance(i[1], dict):
                nx.set_node_attributes(network, i[1], i[0])
            elif isinstance(i[1], tuple):
                nx.set_node_attributes(network, i[1][0], i[0])
            # else:
            #     print(i[0], ":", i[1])

    nx.set_node_attributes(network, statuses, 'Status')
    color_map = {'S': 'green', 'I': 'red', 'R': 'blue'}

    network_graph = hv.Graph.from_networkx(
        network, layout).opts(tools=['hover'], directed=False, node_color='Status', cmap=color_map)

    return network_graph
