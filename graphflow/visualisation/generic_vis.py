# pylint: disable=E1101
import webbrowser

import numpy as np
import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import networkx as nx
import EoN

from graphflow.analysis.metrics import calculate_metric, apply_all_metrics
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
                       metrics: [str] = None, max_time_steps=50):
    hv.extension('bokeh')
    nx_network = get_nx_network(network)

    # remove unused attributes
    for node in nx_network.nodes(data=True):
        del node[1]['infected']
        del node[1]['recovered']

    if simulation_investigation.SIR:
        time_steps = simulation_investigation.t()[1:]
    else:
        time_steps = simulation_investigation.t()[1:max_time_steps]

    spatial_dims = [hv.Dimension('x', range=(-1.1, 1.1)),
                    hv.Dimension('y', range=(-1.1, 1.1))]
    possible_statuses = ["S", "I", "R"]
    color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}
    graph_dict = {}
    node_count = {'S': ([], []), 'I': ([], []), 'R': ([], [])}

    layout = nx.layout.spring_layout(nx_network)
    for time in time_steps:
        statuses = simulation_investigation.get_statuses(time=time)
        nx.set_node_attributes(network, statuses, 'Status')
        apply_all_metrics("epidemic", metrics, nx_network)

        graph = hv.Graph.from_networkx(network, layout).opts(node_color='Status', cmap=color_map)
        graph_dict[time] = graph

        for status in possible_statuses:
            count = len([node for node in nx_network.nodes(data=True) if node[1]['Status'] == status])
            node_count[status][0].append(time)
            node_count[status][1].append(count)

    curve_dict = {status: hv.Curve(node_count[status], key_dimensions=['Time'], value_dimensions=['Count'])
                  for status in possible_statuses}
    ndoverlay = hv.NdOverlay(curve_dict, key_dimensions=[hv.Dimension('Status', values=possible_statuses)])

    distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Counts', label='SRI')
                               for i in time_steps}, key_dimensions=['Time'])

    hmap = hv.HoloMap(graph_dict, key_dimensions=['Time']).relabel(group='Network', label='SRI')

    # defaults = dict(width=700, height=700, padding=0.1)
    # hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    filename = "graph.html"
    hv.save(hmap + distribution, filename, backend='bokeh')
    webbrowser.open(filename)


def __get_epidemic_network_graph(network, layout, statuses, metrics: [str] = None):

    nx.set_node_attributes(network, statuses, 'Status')
    color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}

    apply_all_metrics("epidemic", metrics, network)

    counts = {}
    for status in "SIR":
        count = len([node for node in network.nodes(data=True) if node['Status'] == status])
        counts[status] = count

    network_graph = hv.Graph.from_networkx(
        network, layout).opts(node_color='Status', cmap=color_map, show_legend=True, legend_position='right')

    return network_graph, counts
