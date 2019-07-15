# pylint: skip-file
import webbrowser

from abc import ABC, abstractmethod

import networkx as nx
import holoviews as hv


class Network(ABC):
    _model: str
    _is_calculated: bool = False
    _metrics: [str] = None
    _calculated_networks = {}

    @property
    def model(self):
        return self._model

    @property
    def metrics(self):
        return self._metrics

    @property
    def is_calculated(self):
        return self._is_calculated

    @abstractmethod
    def get_nx_network(self):
        pass

    @abstractmethod
    def calculate(self):
        pass

    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        layout = self._get_hv_network()

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        webbrowser.open(filename)

    def export(self, path):
        pass

    def _get_hv_network(self, color_by=None, color_map=None):
        '''Returns holoviews object from network'''

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
        # TODO make it dynamic - no adding to HTML then, we have to use holoviews
        with open(path_to_html, "a") as file:
            for name, metric in list(self._calculated_networks.values())[0].graph.items():
                file.write("{}: {}<br>".format(name, metric))