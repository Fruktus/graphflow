# pylint: skip-file
"""Contains abstract implementation of network model"""
import csv
import webbrowser

from abc import ABC, abstractmethod

import networkx as nx
import holoviews as hv
import numpy as np
import matplotlib as mpl
import matplotlib.colors as col
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from graphflow.analysis.metric_utils import get_metric, calculate_metric_list


class Network(ABC):
    """
    Abstract class for every model (simple, extended, epidemic, epanet)

    Delivers easy to use and unified inteface for every model

    This class has basic implementation for some methods, mostly ones that are generic enough to be used in all models.
    Being abstract this class can't be instantiated. There are four classes that inherit form this one:
        - graphflow.models.simple.simple_network.SimpleNetwork
        - graphflow.models.extended.extended_network.ExtendedNetwork
        - graphflow.models.epidemic.epidemic_network.EpidemicNetwork
        = graphflow.models.epanet.epanet_network.EpanetNetwork
    See their descriptions for details.
    """

    _model: str
    _is_calculated: bool = False
    _metrics: [str]
    _calculated_networks = {}
    _static_metrics = {}
    _network_properties = {}

    @property
    def model(self):
        """Returns model as string. It can be one of: 'simple', 'extended', 'epidemic' or 'epanet'"""
        return self._model

    @property
    def is_calculated(self):
        """Returns bool indication if the network has been calculated"""
        return self._is_calculated

    @property
    def metrics(self):
        """Returns used metrics as list of strings"""
        return self._metrics

    @abstractmethod
    def get_nx_network(self):
        """Returns base network from the model as networkx graph"""
        pass

    @abstractmethod
    def calculate(self):
        """Calculates network and applies all metrics."""
        pass

    def visualize(self, vis_type: str = 'html'):
        """
            Visualises calculated network

            Args:
                vis_type: What visualisation method should be used. Can be: 'html', 'mp4' or 'gif'. Defaults to
                    'html', 'png'

            Notes:
            In order to export to 'mp4' and 'gif' **imagemagic** is required!

            Different visualization types are supported for different models:
                - simple: 'html'
                - extended: 'html'
                - epidemic: 'html', 'mp4', 'gif', 'png'
                - epanet: has own visualization

            Raises:
                ValueError: Network is not calculated or wrong `vis_type`
        """
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        if vis_type == 'html':
            layout = self._holoviews_get_networks() + self._holoviews_get_metrics()

            filename = "graph.html"
            hv.save(layout, filename, backend='bokeh')
            self._add_metric_list(filename, self._static_metrics)
            webbrowser.open(filename)
        elif vis_type == 'mp4':
            raise ValueError("Visualization type (vis_type) '{}' is unsupported for this model".format(vis_type))
        elif vis_type == 'gif':
            raise ValueError("Visualization type (vis_type) '{}' is unsupported for this model".format(vis_type))
        elif vis_type == 'png':
            raise ValueError("Visualization type (vis_type) '{}' is unsupported for this model".format(vis_type))
        else:
            raise ValueError("Unrecognised vis_type {}".format(vis_type))

    def export(self, filename: str):
        """
        Exports network as CSV file

        Args:
            filename: exported file

        Raises:
            ValueError: Network is not calculated
        """
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            networks = self._calculated_networks

            writer.writerow(['time', 'metrics'] + list(list(networks.values())[0].nodes()))

            for time, net in networks.items():
                data = list(net.nodes(data=True))
                # [(0, {'foo': 'bar'}), (1, {'time': '5pm'}), (2, {})]

                metrics = {}
                for nodes in data:
                    for name, v in nodes[1].items():
                        if name not in metrics:
                            metrics[name] = {}
                        metrics[name][nodes[0]] = v
                # {'foo': {0: 'bar', 1: 'els'}, 'bar': {0: 'bar', 1: 'els'}}

                for name, nodes in metrics.items():
                    row = [time, name]
                    for _, value in nodes.items():
                        row.append(value)
                    writer.writerow(row)

    def _apply_static_metrics(self, network):
        """
        Applies all static metrics to `network` as attributes and fills `_static_metrics` dictionary with not node
        specific metrics.
        """
        if not self.metrics:
            return

        calculated_metrics = calculate_metric_list(network, self.metrics, metric_type='static',
                                                   **self._network_properties)

        for name, value in calculated_metrics.items():
            if isinstance(value, dict):
                nx.set_node_attributes(network, value, name)
            else:
                self._static_metrics[name] = value

    def _apply_dynamic_metrics(self, network):
        """
        Applies all dynamic metrics to `network` as node attributes and not node specific metrics as graph attributes
        """
        if not self.metrics:
            return

        calculated_metrics = calculate_metric_list(network, self.metrics, metric_type='dynamic',
                                                   **self._network_properties)

        for name, value in calculated_metrics.items():
            if isinstance(value, dict):
                nx.set_node_attributes(network, value, name)
            else:
                network.graph[name] = value

    def _holoviews_get_networks(self, color_by=None, color_map=None):
        """
        Returns holovies graph of th network

        Args:
            color_by: Node attribute by by which value it will be colored. If None nodes will not be colored.
                Defaults to None
            color_map: Dictionary {attribute: color} shows what color will nodes have. If color_by is None it will
                be ignored. If None default colors will be used, which vary depending on color_by attribute value

        Returns:
            holoviews.HoloMap: holoviews object representing plot
        """
        hv.extension('bokeh')

        graph_dict = {}
        graph_layout = nx.drawing.layout.spring_layout(list(self._calculated_networks.values())[0])
        for time, graph in self._calculated_networks.items():

            if color_map:
                graph = hv.Graph.from_networkx(self._calculated_networks[time], graph_layout)\
                    .opts(node_color=color_by, cmap=color_map)
            else:
                graph = hv.Graph.from_networkx(self._calculated_networks[time], graph_layout)\
                    .opts(node_color=color_by)
            graph_dict[time] = graph

        holomap = hv.HoloMap(graph_dict, kdims='Time').opts(width=700, height=700, padding=0.1,
                                                            node_size=10, edge_line_width=0.5).relabel(group='Network')

        return holomap

    def _holoviews_get_metrics(self, color_map: dict = {}, label_map: dict = {}):
        """
            Creates holoviews plot for every not node specific metric over time

        Returns:
            holoviews.HoloMap: holoviews object representing plot

        """
        metric_names = [name for name in next(iter(self._calculated_networks.values())).graph.keys()]
        curve_dict = {}
        for metric_name in metric_names:
            name = label_map.get(metric_name, metric_name)
            curve_dict[name] = hv.Curve((list(self._calculated_networks.keys()),
                                                list(map(lambda x: x.graph[metric_name],
                                                         self._calculated_networks.values()))),
                                               kdims='Time', vdims='Value')
            if metric_name in color_map:
                curve_dict[name].opts(color=color_map[metric_name])

        ndoverlay = hv.NdOverlay(curve_dict)
        distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Metrics')
                                   for i in self._calculated_networks.keys()}, kdims='Time')\
            .opts(width=400, height=400, padding=0.1)

        return distribution

    def _save_as_animation(self, filename: str, color_by: str, color_map: dict = {}, label_map: dict = {}):
        """
        Saves calculated networks as mp4 file

        Args:
            filename: filename to save mp4
            color_by: By which attribute nodes should be colored
            color_map: Dictionary {attribute: color} shows what color will nodes have. If None default colors will be
                used, which vary depending on color_by attribute value. Defaults to None
            label_map: Dictionary {attribute: label}. What labels to show in metrics plot. Dict key is name of graph
                attribute, value is label of that attribute in plot
        """
        first_network = next(iter(self._calculated_networks.values()))
        steps = len(self._calculated_networks)

        mpl_cmap = col.ListedColormap(list(color_map.values()))
        color_nums = {value: num for num, value in enumerate(color_map.keys())}

        colors = np.ndarray((steps, len(first_network.nodes())), dtype=int)
        for i, network in enumerate(self._calculated_networks.values()):
            for j, node in enumerate(network.nodes):
                statuses = nx.get_node_attributes(network, color_by)
                if color_map:
                    colors[i, j] = color_nums[statuses[node]]
                else:
                    colors[i, j] = hash(statuses[node])

        fig, (ax_plot, ax_network) = plt.subplots(1, 2, figsize=[10, 5])

        metric_names = [name for name in next(iter(self._calculated_networks.values())).graph.keys()]
        for metric_name in metric_names:
            name = label_map.get(metric_name, metric_name)
            x = list(self._calculated_networks.keys())
            y = list(map(lambda x: x.graph[metric_name], self._calculated_networks.values()))
            ax_plot.plot(x, y, label=name, color=color_map[metric_name])
        ax_plot.legend()
        ax_plot.set_xlabel('Time = 0')
        ax_plot.set_ylabel('Value')

        line = ax_plot.axvline(x=0)

        pos = nx.spring_layout(first_network)
        nodes = nx.draw_networkx_nodes(first_network, pos, ax=ax_network, node_size=10, node_color=colors[0],
                                       cmap=mpl_cmap)
        edges = nx.draw_networkx_edges(first_network, pos, ax=ax_network, width=0.15)
        ax_network.axis("off")

        def update(frames):
            i, time = frames
            line.set_xdata(time)
            nodes.set_array(colors[i])
            ax_plot.set_xlabel('Time = ' + str(time))
            return nodes, line

        data_to_frames = list(enumerate(self._calculated_networks.keys()))
        ani = FuncAnimation(fig, update, interval=5, frames=data_to_frames, blit=True)
        ani.save(filename, writer='imagemagick', savefig_kwargs={'facecolor': 'white'}, fps=10)

    def _save_as_png(self, filename, color_by: str, color_map: dict = {}, label_map: dict = {}):
        networks_as_list = list(self._calculated_networks.values())
        first_network = networks_as_list[0]
        last_network = networks_as_list[-1]

        steps = len(self._calculated_networks)

        mpl_cmap = col.ListedColormap(list(color_map.values()))
        color_nums = {value: num for num, value in enumerate(color_map.keys())}

        first_colors = np.ndarray((len(first_network.nodes()),), dtype=int)
        last_colors = np.ndarray((len(first_network.nodes()),), dtype=int)

        for i, (node1, node2) in enumerate(zip(first_network.nodes, last_network.nodes)):
            statuses1 = nx.get_node_attributes(first_network, color_by)
            statuses2 = nx.get_node_attributes(last_network, color_by)
            if color_map:
                first_colors[i] = color_nums[statuses1[node1]]
                last_colors[i] = color_nums[statuses2[node2]]
            else:
                first_colors[i] = hash(statuses1[node1])
                last_colors[i] = hash(statuses2[node2])

        fig, (ax_plot, ax_first_network, ax_last_network) = plt.subplots(3, 1, figsize=[6, 10])

        metric_names = [name for name in first_network.graph.keys()]
        for metric_name in metric_names:
            name = label_map.get(metric_name, metric_name)
            x = list(self._calculated_networks.keys())
            y = list(map(lambda x: x.graph[metric_name], self._calculated_networks.values()))
            ax_plot.plot(x, y, label=name, color=color_map[metric_name])
        ax_plot.legend()
        ax_plot.set_xlabel('Time')
        ax_plot.set_ylabel('Value')

        pos = nx.spring_layout(first_network)
        first_nodes = nx.draw_networkx_nodes(first_network, pos, ax=ax_first_network, node_size=10,
                                             node_color=first_colors, cmap=mpl_cmap)
        last_nodes = nx.draw_networkx_nodes(last_network, pos, ax=ax_last_network, node_size=10,
                                            node_color=last_colors, cmap=mpl_cmap)
        first_edges = nx.draw_networkx_edges(first_network, pos, ax=ax_first_network, width=0.15)
        last_edges = nx.draw_networkx_edges(last_network, pos, ax=ax_last_network, width=0.15)
        ax_first_network.axis("off")
        ax_first_network.set_title('Beginning of simulation', pad=-180.0)
        ax_last_network.axis("off")
        ax_last_network.set_title('End of simulation', pad=-180.0)

        fig.savefig(filename)

    def _add_metric_list(self, path_to_html: str, metrics_to_add: dict):
        """
        Appends to html list of all metrics

        Html should have been created before and should already contain network visualization.

        Args:
            path_to_html: path to html to append
            metrics_to_add: dictionary of metrics to add {name: value}
        """
        with open(path_to_html, "a") as file:
            for name, metric in metrics_to_add.items():
                file.write("{}: {}<br>".format(name, metric))
