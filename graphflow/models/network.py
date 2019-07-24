# pylint: skip-file
"""Contains abstract implementation of network model"""
import csv
import webbrowser

from abc import ABC, abstractmethod

import networkx as nx
import holoviews as hv

from graphflow.analysis.metric_utils import get_metric, calculate_metric_list


class Network(ABC):
    """
    Abstract class for every model (simple, extended, epidemic, epanet)

    Delivers easy to use interface and unified for every model.
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

    def visualize(self):
        """
            Visualises calculated network

            Raises:
                ValueError: Network is not calculated
        """
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        layout = self._get_hv_network() + self._get_metrics_plot()

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        self._add_metric_list(filename, self._static_metrics)
        webbrowser.open(filename)

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

    def _get_hv_network(self, color_by=None, color_map=None):
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

        holomap = hv.HoloMap(graph_dict, kdims='Time').opts(width=700, height=700, padding=0.1).relabel(group='Network')

        return holomap

    def _get_metrics_plot(self, color_map: dict = {}, label_map: dict = {}):
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
