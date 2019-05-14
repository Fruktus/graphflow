from enum import Enum
import wntr
from wntr.network import WaterNetworkModel
from wntr.sim import SimulationResults


class SimulationType(Enum):
    PRESSURE = "pressure"
    QUALITY = "quality"


class EpanetFlowNetwork:
    water_network_model: WaterNetworkModel
    simulation_type: SimulationType
    results: SimulationResults
    hours: int
    trace_node: str

    def __init__(self, path_to_network_file, simulation_type, **kwargs):
        self.water_network_model = wntr.network.WaterNetworkModel(path_to_network_file)
        self.simulation_type = simulation_type
        self.hours = kwargs.get('time', None)
        self.trace_node = kwargs.get('trace_node', None)

    def run_simulation(self):
        if self.simulation_type == SimulationType.PRESSURE:
            self.__simulate_pressure()
        if self.simulation_type == SimulationType.QUALITY:
            self.__simulate_quality()

    def __simulate_quality(self):
        if self.trace_node is None:
            raise ValueError('No trace node has been passed')
        self.water_network_model.options.quality.mode = 'TRACE'
        self.water_network_model.options.quality.trace_node = self.trace_node
        self.__simulate()

    def __simulate_pressure(self):
        if self.hours is None:
            raise ValueError('No time range has been passed')
        self.__simulate()

    def __simulate(self):
        sim = wntr.sim.EpanetSimulator(self.water_network_model)
        self.results = sim.run_sim()

    def get_networkx_graph(self):
        return self.water_network_model.get_graph()
