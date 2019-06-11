import EoN
import networkx as nx
import matplotlib.pyplot as plt
from graphflow.epidemic import epidemic_runner
from enum import Enum


class Simulation():
    sim_params: epidemic_runner.ExperimentParameters

    def __init__(self, sim_params):
        self.simulation_params = sim_params

    def run_simulation(self):
        if self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIR:
            simulation = EoN.fast_SIR(self.simulation_params.network,
                                      self.simulation_params.edge_transmission_rate,
                                      self.simulation_params.node_recovery_rate,
                                      initial_infecteds=self.simulation_params.initial_infected,
                                      initial_recovereds=self.simulation_params.initial_recovered,
                                      rho=None,
                                      tmin=0,
                                      tmax=float('Inf'),
                                      transmission_weight=None,
                                      recovery_weight=None,
                                      return_full_data=True)

        elif self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIS:
            simulation = EoN.fast_SIS(self.simulation_params.network,
                                      self.simulation_params.edge_transmission_rate,
                                      self.simulation_params.node_recovery_rate,
                                      initial_infecteds=self.simulation_params.initial_infected,
                                      rho=None,
                                      tmin=0,
                                      tmax=self.simulation_params.tmax,
                                      transmission_weight=None,
                                      recovery_weight=None,
                                      return_full_data=True)



        else:
            pass

        animation = simulation.animate()
        # pos = {node: node for node in self.simulation_params.network}
        # simulation.set_pos(pos)
        # animation = simulation.animate(ts_plots=['I', 'SIR'], node_size=4)
        animation.save('amination_out11.mp4', fps=5, extra_args=['-vcodec', 'libx264'])


# my_sim = Simulation(epidemic_runner.simulation_input_data)
# my_sim.run_simulation()






