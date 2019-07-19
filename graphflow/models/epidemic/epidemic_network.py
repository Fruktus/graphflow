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
        self._apply_static_metrics()

        for key in list(nx_network.graph.keys()):
            del nx_network.graph[key]

        for time, s, i, r in zip(self.__time_steps, self.__S, self.__I, self.__R):
            self._calculated_networks[time] = deepcopy(nx_network)

            if self._metrics:
                apply_all_metrics(self._model, self._metrics, self._calculated_networks[time])

            statuses = self.__simulation_investigation.get_statuses(time=time)
            nx.set_node_attributes(self._calculated_networks[time], statuses, 'status')

        self._apply_dynamic_metrics()
        self._is_calculated = True

    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        color_map = {'S': 'yellow', 'I': 'red', 'R': 'green'}
        layout = self._get_hv_network(color_by="status", color_map=color_map) + \
            self._get_hv_plot(color_map)

        if list(self._calculated_networks.values())[0].graph.keys():
            layout += self._get_metrics_plot()

        filename = "graph.html"
        hv.save(layout, filename, backend='bokeh')
        self._add_metric_list(filename)
        webbrowser.open(filename)

    def _get_hv_plot(self, color_map: dict):
        """
        Creates holoviews plot for each of the S, I and R states

        Plot shows how many nodes are Susceptible (S), Infected (I) and Recovered (R) over time. It also contains
        line to mark in which moment in time we are.

        Args:
            color_map: dictionary {state: color}, shows how to color nodes. state can be 'S', 'I' or 'R'

        Returns:
            holoviews.HoloMap: holoviews object representing plot

        """

        curve_dict = {'Susceptible': hv.Curve((self.__time_steps, self.__S), kdims='Time', vdims='Count')\
                      .opts(color=color_map['S']),
                      'Infected ': hv.Curve((self.__time_steps, self.__I), kdims='Time', vdims='Count').opts(
                          color=color_map['I'])}

        if self.__simulation_investigation.SIR:
            curve_dict['Recovered '] = hv.Curve((self.__time_steps, self.__R), kdims='Time', vdims='Count').opts(
                color=color_map['R'])

        ndoverlay = hv.NdOverlay(curve_dict)
        distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Counts')
                                   for i in self.__time_steps}, kdims='Time').opts(width=400, height=400, padding=0.1)

        return distribution

    def _get_metrics_plot(self):
        """
            Creates holoviews plot for every not node specific metric over time

        Returns:
            holoviews.HoloMap: holoviews object representing plot

        """
        metric_names = [name for name in list(self._calculated_networks.values())[0].graph.keys()]
        metric_dict = {}
        for metric_name in metric_names:
            metric_dict[metric_name] = []
        for time, network in self._calculated_networks.items():
            for name, metric in network.graph.items():
                metric_dict[name].append(metric)
        curve_dict = {}
        for metric_name in metric_names:
            curve_dict[metric_name] = hv.Curve((self.__time_steps, metric_dict[metric_name]), kdims='Time', vdims='Value')

        ndoverlay = hv.NdOverlay(curve_dict)
        distribution = hv.HoloMap({i: (ndoverlay * hv.VLine(i)).relabel(group='Metrics')
                                   for i in self.__time_steps}, kdims='Time').opts(width=400, height=400, padding=0.1)

        return distribution
