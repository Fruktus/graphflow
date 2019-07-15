# pylint: disable=E1101
import webbrowser

import networkx as nx
import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import EoN

from graphflow.analysis.metrics import apply_all_metrics
from graphflow.analysis.network_utils import get_nx_network


def visualize_holoviews(network, metrics: [tuple] = None):
    """generates interactive html plot of network
    :param network: networkx graph
    :param metrics: an array of two-tuple consisting of string (metric name) and dict or value returned from metric
    """
    hv.extension('bokeh')

    nx_network = get_nx_network(network)
    if metrics:
        for i in metrics:
            if isinstance(i, dict):
                nx.set_node_attributes(nx_network, i)
            elif isinstance(i[1], dict):
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
        time_steps = simulation_investigation.t()[0:]
    else:
        time_steps = simulation_investigation.t()[0:max_time_steps]

    possible_statuses = ["S", "I", "R"]
    color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}
    graph_dict = {}
    metrics_dict = {}
    node_count = {'S': ([], []), 'I': ([], []), 'R': ([], [])}

    layout = nx.layout.spring_layout(nx_network)
    for time in time_steps:
        statuses = simulation_investigation.get_statuses(time=time)
        nx.set_node_attributes(network, statuses, 'Status')
        apply_all_metrics("epidemic", metrics, nx_network)

        labels = hv.Labels({(0, i/2-0.9): "{}: {}".format(metric, value)
                            for i, (metric, value) in enumerate(nx_network.graph.items())
                            if metric not in ('bottom', 'top')})
        metrics_dict[time] = labels

        graph = hv.Graph.from_networkx(network, layout).opts(node_color='Status', cmap=color_map)
        graph_dict[time] = graph

        for status in possible_statuses:
            count = len([node for node in nx_network.nodes(data=True) if node[1]['Status'] == status])
            node_count[status][0].append(time)
            node_count[status][1].append(count)

    curve_dict = {status: hv.Curve(node_count[status], kdims='Time', vdims='Count').opts(color=color_map[status])
                  for status in possible_statuses}
    ndoverlay = hv.NdOverlay(curve_dict)
    distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Counts')
                               for i in time_steps}, kdims='Time').opts(width=400, height=400, padding=0.1)

    holomap = hv.HoloMap(graph_dict, kdims='Time').opts(width=400, height=400, padding=0.1).relabel(group='Network')
    labels_holomap = hv.HoloMap(metrics_dict, kdims='Time').opts(xaxis=None, yaxis=None, height=100)

    layout = (holomap + distribution + labels_holomap).cols(2)

    filename = "graph.html"
    hv.save(layout, filename, backend='bokeh')
    webbrowser.open(filename)
