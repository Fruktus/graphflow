# pylint: skip-file
import csv
import webbrowser

from abc import ABC, abstractmethod

import networkx as nx
import holoviews as hv

from graphflow.analysis.metric_utils import get_metric


class Network(ABC):
    """
    Abstract class for every model (simple, extended, epidemic, epanet)

    Delivers easy to use interface for every model.
    """
    _model: str
    _is_calculated: bool = False
    _metrics: [str] = None
    _calculated_networks = {}
    _calculated_metrics = {}
    _static_metrics = {}

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

    @property
    def calculated_metrics(self):
        """
        Returns calculated metrics

        Raises:
            ValueError: Network is not calculated
        """
        if not self.is_calculated:
            raise ValueError("Network not calculated")
        return self._calculated_metrics

    @property
    def calculated_networks(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated")
        return self._calculated_networks

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

        layout = self._get_hv_network()

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        self._add_metric_list(filename)
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
        Applies all static metrics to `network` as attributes and fills
        `_static_metrics` dictionary with not node specific metrics.
        """
        if not self.metrics:
            return

        for name in self.metrics:
            fun, model, metric_type = get_metric(name, details=True)
            if metric_type == 'static':
                value = fun(network)
                if isinstance(value, dict):
                    nx.set_node_attributes(network, value, name)
                else:
                    self._static_metrics[name] = value

    def _apply_dynamic_metrics(self):
        """
        Applies all dynamic metrics to `_calculated_graphs` dictionary as node attributes and not node specific
        metrics as graph attributes
        """
        if not self.metrics:
            return

        funs = []
        for name in self.metrics:
            fun, model, metric_type = get_metric(name, details=True)
            if metric_type == 'dynamic':
                funs.append(fun)

        for network in self.calculated_networks:
            for fun in funs:
                value = fun(network)
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

        holomap = hv.HoloMap(graph_dict, kdims='Time').opts(width=400, height=400, padding=0.1).relabel(group='Network')

        return holomap

    def _add_metric_list(self, path_to_html):
        """
        Appends to html list of all not node specific metrics.

        Html is should have been created before and should already contain network visualization.

        Args:
            path_to_html: path to html to append

        """
        with open(path_to_html, "a") as file:
            for name, metric in self._static_metrics.values():
                file.write("{}: {}<br>".format(name, metric))
