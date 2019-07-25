# pylint: skip-file
""""Contains implementation for epidemic model"""
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

    Depending on arguments this class can calculate spreading infection using different methods from EoN library:
        - `fast_SIR(G, tau, gamma[, initial_infecteds, …])` - simulation_type='sir', algorithm='fast'
        - `fast_SIS(G, tau, gamma[, initial_infecteds, …])` - simulation_type='sis', algorithm='fast'
        - `basic_discrete_SIR(G, p[, …])` - simulation_type='sir', algorithm='discrete'
        - `basic_discrete_SIS(G, p[, …])` - simulation_type='sir', algorithm='discrete'

    Args:
        path_to_network: Path to file containing network in GML format. Each node requires attributes: 'infected'
            (for SIR ans SIS) and 'recovered' (for SIR only). Each of them is either 0 or 1.
        metrics: Used metrics as list of strings. Each name has to be name of one of the functions in on of the
            ``graphflow.analysis.metrics`` and ``graphflow.analysis.epidemic_metrics`` files
        *args: Not used in this model
        **kwargs: See below

    Keyword Args:
        simulation_type (str): Required. 'sis' or 'sir'
        algorithm (str): Required. 'fast' or 'discrete'.
        transmission_rate (float): Required for **fast** algorithm. Transmission rate per edge
        recovery_rate (float): Required for **fast** algorithm. Recovery rate per node
        transmission_probability (float): Required for **discrete** algorithm. Transmission probability
        max_time (float): Maximal simulation time. Defaults to `Inf`. It has to be specified for SIS model since or it will
            run infinitely.

    See Also:
        https://epidemicsonnetworks.readthedocs.io/en/latest/EoN.html

    Examples:
        >>> network = EpidemicNetwork('network.txt', ['degree_centrality', 'diameter'], simulation_type='sis', \
        ... algorithm='fast', transmission_rate=2.0, recovery_rate=1.0, max_time=2.0)
        >>> network.calculate()
        >>> network.visualize()
        >>> network.export('exported.csv')
    """

    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'epidemic'
        self._metrics = metrics
        self.__simulation_investigation = None
        transmission_rate = kwargs.get('transmission_rate', None)
        recovery_rate = kwargs.get('recovery_rate', None)
        transmission_probability = kwargs.get('transmission_probability', None)
        max_time = kwargs.get('max_time', float('Inf'))

        self._network_properties['simulation_type'] = kwargs['simulation_type']
        self._network_properties['algorithm'] = kwargs['algorithm']
        if transmission_rate:
            self._network_properties['transmission_rate'] = transmission_rate
        if recovery_rate:
            self._network_properties['recovery_rate'] = recovery_rate
        if transmission_probability:
            self._network_properties['transmission_probability'] = transmission_probability
        if max_time:
            self._network_properties['max_time'] = max_time

        epidemic_params = Parser()
        epidemic_params.parse_input(kwargs['simulation_type'], kwargs['algorithm'], path_to_network,
                                    transmission_rate=transmission_rate,
                                    recovery_rate=recovery_rate,
                                    transmission_probability=transmission_probability,
                                    max_time=max_time)
        simulation_config = epidemic_params.get_simulation_config()

        self.__my_sim = Simulation(simulation_config)

    def get_nx_network(self):
        return self.__my_sim.get_network()

    def calculate(self):
        lg.info('starting calculation')
        self.__simulation_investigation = self.__my_sim.run_simulation()

        if self.__simulation_investigation.SIR:
            time_steps, S, I, R = self.__simulation_investigation.summary()
            time_steps = time_steps[1:]
        else:
            time_steps, S, I = self.__simulation_investigation.summary()
            R = [0 for _ in time_steps]

        if time_steps[0] == -1.0:
            time_steps = time_steps[1:]
            S = S[1:]
            I = I[1:]
            R = R[1:]

        nx_network = self.get_nx_network()

        for key in list(nx_network.graph.keys()):
            del nx_network.graph[key]

        first_iter = True
        for time, s, i, r in zip(time_steps, S, I, R):
            self._calculated_networks[time] = deepcopy(nx_network)

            self._calculated_networks[time].graph['S'] = s
            self._calculated_networks[time].graph['I'] = i
            if self.__simulation_investigation.SIR:
                self._calculated_networks[time].graph['R'] = r

            statuses = self.__simulation_investigation.get_statuses(time=time)
            nx.set_node_attributes(self._calculated_networks[time], statuses, 'status')

            if first_iter:
                nx_network = self._calculated_networks[time]
                self._apply_static_metrics(nx_network)
                first_iter = False

            # this method uses 'status' attribute added in two previous lines
            self._apply_dynamic_metrics(self._calculated_networks[time])

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
        lg.info('visualization done')
        webbrowser.open(filename)

    def animate(self):
        return self.__my_sim.animation

