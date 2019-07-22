import uuid
# from EoN import fast_SIR, fast_SIS
from graphflow.models.epidemic.custom_simulation import fast_SIR, fast_SIS
from graphflow.models.epidemic import epidemic_runner


class Simulation:
    simulation_params: epidemic_runner.ExperimentParameters

    def __init__(self, sim_params, seed=None, probability=None):
        self.simulation_params = sim_params
        self.seed = seed
        self.probability = probability

    def get_network(self):
        return self.simulation_params.network

    def run_simulation(self, save_to_file=False):
        if self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIR:
            simulation = fast_SIR(self.simulation_params.network,
                                  self.simulation_params.edge_transmission_rate,
                                  self.simulation_params.node_recovery_rate,
                                  initial_infecteds=self.simulation_params.initial_infected,
                                  initial_recovereds=self.simulation_params.initial_recovered,
                                  rho=None,
                                  tmin=0,
                                  tmax=float('Inf'),
                                  transmission_weight=None,
                                  recovery_weight=None,
                                  return_full_data=True,
                                  seed=self.seed,
                                  probability=self.probability)

        elif self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIS:
            simulation = fast_SIS(self.simulation_params.network,
                                  self.simulation_params.edge_transmission_rate,
                                  self.simulation_params.node_recovery_rate,
                                  initial_infecteds=self.simulation_params.initial_infected,
                                  rho=None,
                                  tmin=0,
                                  tmax=self.simulation_params.tmax,
                                  transmission_weight=None,
                                  recovery_weight=None,
                                  return_full_data=True,
                                  seed=self.seed,
                                  probability=self.probability
                                  )

        else:
            raise NotImplementedError

        animation = simulation.animate()

        if save_to_file:
            unique_filename = str(uuid.uuid4())
            animation.save(unique_filename + '.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

        return simulation
