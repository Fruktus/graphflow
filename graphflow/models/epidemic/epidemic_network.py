# pylint: skip-file
import webbrowser
from copy import deepcopy

import networkx as nx
import holoviews as hv

from graphflow.analysis.metric_utils import apply_all_metrics
from graphflow.models.epidemic.epidemic_runner import Parser
from graphflow.models.epidemic.epidemic_simulation import Simulation
from graphflow.models.network import Network


class EpidemicNetwork(Network):
    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'epidemic'
        self._metrics = metrics
        self.__simulation_investigation = None
        self.__time_steps = None
        self.__S = None
        self.__I = None
        self.__R = None

        epidemic_params = Parser()
        epidemic_params.parse_input(args[0], path_to_network, *args[1:])
        simulation_config = epidemic_params.get_simulation_config()

        self.__my_sim = Simulation(simulation_config)

    def get_nx_network(self):
        return self.__my_sim.get_network()

    def calculate(self):
        self.__simulation_investigation = self.__my_sim.run_simulation()

        if self.__simulation_investigation.SIR:
            self.__time_steps, self.__S, self.__I, self.__R = self.__simulation_investigation.summary()
            self.__time_steps = self.__time_steps[1:]
            self.__S = self.__S[1:]
            self.__I = self.__I[1:]
            self.__R = self.__R[1:]
        else:
            self.__time_steps, self.__S, self.__I = self.__simulation_investigation.summary()
            self.__R = [0 for i in self.__time_steps]

        nx_network = self.get_nx_network()
        for time, s, i, r in zip(self.__time_steps, self.__S, self.__I, self.__R):
            self._calculated_networks[time] = deepcopy(nx_network)

            if self._metrics:
                apply_all_metrics(self._model, self._metrics, self._calculated_networks[time])

            self._calculated_networks[time].graph['S'] = s
            self._calculated_networks[time].graph['I'] = i
            if self.__simulation_investigation.SIR:
                self._calculated_networks[time].graph['R'] = r

            statuses = self.__simulation_investigation.get_statuses(time=time)
            nx.set_node_attributes(self._calculated_networks[time], statuses, 'status')

        self._is_calculated = True

    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}
        layout = self._get_hv_network(color_by="status", color_map=color_map) + self._get_hv_plot(color_map)

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        self._add_metric_list(filename)
        webbrowser.open(filename)

    # TODO implement
    def export(self, path):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

    def _get_hv_plot(self, color_map):
        curve_dict = {}
        curve_dict['S'] = hv.Curve((self.__time_steps, self.__S), kdims='Time', vdims='Count')\
            .opts(color=color_map['S'])
        curve_dict['I'] = hv.Curve((self.__time_steps, self.__I), kdims='Time', vdims='Count').opts(
            color=color_map['I'])
        if self.__simulation_investigation.SIR:
            curve_dict['R'] = hv.Curve((self.__time_steps, self.__R), kdims='Time', vdims='Count').opts(
                color=color_map['R'])

        ndoverlay = hv.NdOverlay(curve_dict)
        distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Counts')
                                   for i in self.__time_steps}, kdims='Time').opts(width=400, height=400, padding=0.1)

        return distribution
