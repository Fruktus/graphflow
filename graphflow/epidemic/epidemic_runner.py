import networkx as nx
from enum import Enum


class EpidemicSimulationType(Enum):
    SIR = "sir"
    SIS = "sis"


class ExperimentParameters():

    def __init__(self, simulation_type, graph, edge_transmission_rate,
                 node_recovery_rate, initial_infected, initial_recovered, tmax):
        self.simulation_type = simulation_type
        self.network = graph
        self.edge_transmission_rate = edge_transmission_rate
        self.node_recovery_rate = node_recovery_rate
        self.initial_infected = initial_infected
        self.initial_recovered = initial_recovered
        self.tmax = tmax


class Parser():
    sym_type: EpidemicSimulationType
    G: nx.Graph
    transm_rate: float
    recov_rate: float
    initial_infected: []
    initial_recovered: []
    t_max: int
    simulation_input_data: ExperimentParameters

    def parse_input(self, type, network, transmission, recovery, maxtime):
        # simulation type
        self.sym_type = None
        if type.lower() == 'sir':
            self.sym_type = EpidemicSimulationType.SIR
        elif type.lower() == 'sis':
            self.sym_type = EpidemicSimulationType.SIS
        else:
            raise ValueError("Invalid simulation type name!")

        # networkx Graph
        gml_graph = network
        self.G = nx.read_gml(gml_graph)

        # transmission rate per edge
        self.transm_rate = transmission

        # recovery rate per node
        self.recov_rate = recovery

        # lists of initialy infected and recovered(only when SIR) nodes
        self.initial_infected = []
        self.initial_recovered = []
        for n in nx.nodes(self.G):
            if self.G.nodes[n]['infected'] == True:
                self.initial_infected.append(n)
            elif self.G.nodes[n]['recovered'] == True:
                self.initial_recovered.append(n)

        # max simulation time
        self.t_max = maxtime


    def get_simulation_config(self):
        self.simulation_input_data = None
        if self.sym_type == EpidemicSimulationType.SIR:
            self.simulation_input_data = ExperimentParameters(self.sym_type, self.G, self.transm_rate, self.recov_rate,
                                                              self.initial_infected,
                                                              self.initial_recovered, self.t_max)
        else:
            self.simulation_input_data = ExperimentParameters(self.sym_type, self.G, self.transm_rate, self.recov_rate,
                                                              self.initial_infected, None,
                                                              self.t_max)

        return self.simulation_input_data
