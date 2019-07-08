import EoN
from graphflow.epidemic import epidemic_runner
import uuid


class Simulation:
    sim_params: epidemic_runner.ExperimentParameters

    def __init__(self, sim_params):
        self.simulation_params = sim_params

    def get_network(self):
        return self.sim_params.network

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
            raise NotImplementedError

        animation = simulation.animate()
        unique_filename = str(uuid.uuid4())
        animation.save(unique_filename + '.mp4', fps=5, extra_args=['-vcodec', 'libx264'])
