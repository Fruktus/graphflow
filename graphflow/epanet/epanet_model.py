# pylint: disable=R0902
from enum import Enum
import numpy as np
import pandas as pd
import wntr
from wntr.network import WaterNetworkModel
from wntr.sim import SimulationResults
from scipy.stats import expon


class SimulationType(Enum):
    PRESSURE = "pressure"
    QUALITY = "quality"
    EARTHQUAKE = "earthquake"


class EpanetFlowNetwork:
    water_network_model: WaterNetworkModel
    simulation_type: SimulationType
    results: SimulationResults
    hours: int
    trace_node: str

    # earthquake parameters
    epicenter: (int, int)
    magnitude: float
    depth: int
    earthquake: wntr.scenario.Earthquake
    distance_to_epicenter: pd.Series
    pga: pd.Series
    pgv: pd.Series
    repair_rate: pd.Series
    length: pd.Series
    pipe_fc: wntr.scenario.FragilityCurve
    pipe_pr: pd.DataFrame
    pipe_damage_state: pd.Series
    pipe_damage_val: pd.Series

    def __init__(self, path_to_network_file, simulation_type, **kwargs):
        self.water_network_model = wntr.network.WaterNetworkModel(path_to_network_file)
        self.simulation_type = simulation_type
        self.hours = kwargs.get('time', None)
        self.trace_node = kwargs.get('trace_node', None)
        self.epicenter = kwargs.get('epicenter', None)
        self.magnitude = kwargs.get('magnitude', None)
        self.depth = kwargs.get('depth', None)

    def run_simulation(self):
        if self.simulation_type == SimulationType.EARTHQUAKE:
            print("Simulating earthquake")
            self.__simulate_earthquake()
        elif self.simulation_type == SimulationType.PRESSURE:
            print("Simulating pressure")
            self.__simulate_pressure()
        elif self.simulation_type == SimulationType.QUALITY:
            print("Simulating quality")
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

    def __simulate_earthquake(self):
        self.water_network_model.scale_node_coordinates(1000)
        self.earthquake = wntr.scenario.Earthquake(self.epicenter, self.magnitude, self.depth)
        self.distance_to_epicenter = \
            self.earthquake.distance_to_epicenter(self.water_network_model, element_type=wntr.network.Pipe)
        self.pga = self.earthquake.pga_attenuation_model(self.distance_to_epicenter)
        self.pgv = self.earthquake.pgv_attenuation_model(self.distance_to_epicenter)
        self.repair_rate = self.earthquake.repair_rate_model(self.pgv)
        self.length = pd.Series(self.water_network_model.query_link_attribute('length', link_type=wntr.network.Pipe))
        self.pipe_fc = wntr.scenario.FragilityCurve()
        self.pipe_fc.add_state('Minor leak', 1, {'Default': expon(scale=0.2)})
        self.pipe_fc.add_state('Major leak', 2, {'Default': expon()})
        self.pipe_pr = self.pipe_fc.cdf_probability(self.repair_rate * self.length)
        pipe_damage_state = self.pipe_fc.sample_damage_state(self.pipe_pr)

        pipe_damage_state_map = self.pipe_fc.get_priority_map()
        self.pipe_damage_val = pipe_damage_state.map(pipe_damage_state_map)

        print("Min, Max, Average PGA: " + str(np.round(self.pga.min(), 2)) + ", " + str(np.round(self.pga.max(), 2))
              + ", " + str(np.round(self.pga.mean(), 2)) + " g")
        print("Min, Max, Average PGV: " + str(np.round(self.pgv.min(), 2)) + ", " + str(np.round(self.pgv.max(), 2))
              + ", " + str(np.round(self.pgv.mean(), 2)) + " m/s")
        print("Min, Max, Average repair rate: " + str(np.round(self.repair_rate.min(), 5))
              + ", " + str(np.round(self.repair_rate.max(), 5)) + ", "
              + str(np.round(self.repair_rate.mean(), 5)) + " per m")
        print("Min, Max, Average repair rate*pipe length: " + str(np.round((self.repair_rate * self.length).min(), 5))
              + ", " + str(np.round((self.repair_rate * self.length).max(), 5)) + ", "
              + str(np.round((self.repair_rate * self.length).mean(), 5)))
        print("Number of pipe failures: " + str(sum(self.pipe_damage_val > 0)))

    def __simulate(self):
        sim = wntr.sim.EpanetSimulator(self.water_network_model)
        self.results = sim.run_sim()

    def get_networkx_graph(self):
        return self.water_network_model.get_graph()
