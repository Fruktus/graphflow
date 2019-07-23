# pylint: skip-file
import webbrowser
from copy import deepcopy
import logging as lg

import networkx as nx
import holoviews as hv

from graphflow.models.epidemic.epidemic_runner import Parser
from graphflow.models.epidemic.epidemic_simulation import Simulation
from graphflow.models.network import Network

lg.getLogger('epidemic')


class EpidemicNetwork(Network):
    """
    EpidemicNetwork implements epidemic model, using EoN library. Both SIR and SIS models are supported.

    Args:
        path_to_network: Path to file containing network in GML format. Each node requires attributes: 'infected'
            (for SIR ans SIS) and 'recovered' (for SIR only). Each of them is either 0 or 1.
        metrics: Used metrics as list of strings. Each name has to be name of one of the functions in on of the
            ``graphflow.analysis.metrics.py`` and ``graphflow.analysis.epidemic_metrics.py`` files
        *args: Specify model (SIR or SIS) and simulation parameters:
            model (str): 'sis' or 'sir'
            transmission (float): Transmission rate per edge
            recovery (float): Recovery rate per node
            maxtime (int): Maximal simulation time. Not used in SIR model.
        **kwargs: Not used in this model

    Examples:
        >>> network = EpidemicNetwork('network.txt', ['degree_centrality', 'diameter'], 'sis', 2.0, 1.0, 2)
        >>> network.calculate()
        >>> network.visualize()
        >>> network.export('exported.csv')
    """

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
        lg.info('starting calculation')
        self.__simulation_investigation = self.__my_sim.run_simulation()

        if self.__simulation_investigation.SIR:
            self.__time_steps, self.__S, self.__I, self.__R = self.__simulation_investigation.summary()
            self.__time_steps = self.__time_steps[1:]
            self.__S = self.__S[1:]
            self.__I = self.__I[1:]
            self.__R = self.__R[1:]
        else:
            self.__time_steps, self.__S, self.__I = self.__simulation_investigation.summary()
            self.__R = [0 for _ in self.__time_steps]

        nx_network = self.get_nx_network()
        self._apply_static_metrics(nx_network)

        for key in list(nx_network.graph.keys()):
            del nx_network.graph[key]

        for time, s, i, r in zip(self.__time_steps, self.__S, self.__I, self.__R):
            self._calculated_networks[time] = deepcopy(nx_network)

            self._calculated_networks[time].graph['S'] = s
            self._calculated_networks[time].graph['I'] = i
            if self.__simulation_investigation.SIR:
                self._calculated_networks[time].graph['R'] = r

            self._apply_dynamic_metrics(self._calculated_networks[time])

            statuses = self.__simulation_investigation.get_statuses(time=time)
            nx.set_node_attributes(self._calculated_networks[time], statuses, 'status')

        self._is_calculated = True
        lg.info('calculation complete')

    def visualize(self):
        lg.info('starting visualization')
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}
        label_map = {'S': 'Susceptible', 'I': 'Infected', 'R': 'Recovered'}
        layout = self._get_hv_network(color_by="status", color_map=color_map) + \
            self._get_metrics_plot(color_map=color_map, label_map=label_map)

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        self._add_metric_list(filename, self._static_metrics)
        webbrowser.open(filename)
