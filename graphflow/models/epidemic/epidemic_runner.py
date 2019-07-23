# pylint: skip-file

from enum import Enum
import networkx as nx


class EpidemicSimulationType(Enum):
    SIR = 'sir'
    SIS = 'sis'


class Algorithm(Enum):
    FAST = 'fast'
    DISCRETE = 'discrete'


class ExperimentParameters:

    def __init__(self,
                 simulation_type,
                 algorithm,
                 network,
                 initial_infected,
                 initial_recovered,
                 transmission_rate=None,
                 recovery_rate=None,
                 transmission_probability=None,
                 max_time=float('Inf')):

        self.simulation_type = simulation_type
        self.algorithm = algorithm
        self.network = network
        self.initial_infected = initial_infected
        self.initial_recovered = initial_recovered
        self.transmission_rate = transmission_rate
        self.recovery_rate = recovery_rate
        self.transmission_probability = transmission_probability
        self.max_time = max_time


class Parser:
    sym_type: EpidemicSimulationType
    algorithm: Algorithm
    network: nx.Graph
    transmission_rate: float
    recovery_rate: float
    transmission_probability: float
    initial_infected: []
    initial_recovered: []
    max_time: float
    simulation_input_data: ExperimentParameters

    def parse_input(self, sim_type, algorithm, path_to_network,
                    transmission_rate=None, recovery_rate=None, transmission_probability=None, max_time=float('Inf')):

        # simulation type
        self.sym_type = None
        if sim_type.lower() == 'sir':
            self.sym_type = EpidemicSimulationType.SIR
        elif sim_type.lower() == 'sis':
            self.sym_type = EpidemicSimulationType.SIS
        else:
            raise ValueError("Invalid simulation type name!")

        # algorithm
        self.algorithm = None
        if algorithm.lower() == 'fast':
            self.algorithm = Algorithm.FAST
        elif algorithm.lower() == 'discrete':
            self.algorithm = Algorithm.DISCRETE
        else:
            raise ValueError("Invalid algorithm!")

        # networkx Graph
        gml_graph = path_to_network
        self.network = nx.read_gml(gml_graph)

        # transmission rate per edge
        self.transmission_rate = transmission_rate

        # recovery rate per node
        self.recovery_rate = recovery_rate

        # Infection probability
        self.transmission_probability = transmission_probability

        # check if correct args
        if algorithm == Algorithm.FAST:
            if not transmission_rate:
                raise ValueError("Transmission rate is required for fast algorithm!")
            if not recovery_rate:
                raise ValueError("Recovery rate is required for fast algorithm!")
        elif algorithm == Algorithm.DISCRETE:
            if not transmission_probability:
                raise ValueError("Transmission probability is required for discrete algorithm")

        # lists of initially infected and recovered(only when SIR) nodes
        self.initial_infected = []
        self.initial_recovered = []
        for n in nx.nodes(self.network):
            if self.network.nodes[n]['infected']:
                self.initial_infected.append(n)
            elif self.network.nodes[n]['recovered']:
                self.initial_recovered.append(n)
        if self.sym_type == EpidemicSimulationType.SIS:
            self.initial_recovered = None

        # max simulation time
        self.max_time = max_time

    def get_simulation_config(self):
        self.simulation_input_data = ExperimentParameters(simulation_type=self.sym_type,
                                                          algorithm=self.algorithm,
                                                          network=self.network,
                                                          initial_infected=self.initial_infected,
                                                          initial_recovered=self.initial_recovered,
                                                          transmission_rate=self.transmission_rate,
                                                          recovery_rate=self.recovery_rate,
                                                          transmission_probability=self.transmission_probability,
                                                          max_time=self.max_time)

        return self.simulation_input_data
