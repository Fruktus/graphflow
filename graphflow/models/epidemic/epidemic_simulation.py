import uuid
from EoN import fast_SIR, fast_SIS, basic_discrete_SIR, basic_discrete_SIS
# from graphflow.models.epidemic.custom_simulation import fast_SIR, fast_SIS, basic_discrete_SIR, basic_discrete_SIS
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

        if self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIR and \
                self.simulation_params.algorithm == epidemic_runner.Algorithm.FAST:
            simulation = fast_SIR(self.simulation_params.network,
                                  tau=self.simulation_params.transmission_rate,
                                  gamma=self.simulation_params.recovery_rate,
                                  initial_infecteds=self.simulation_params.initial_infected,
                                  initial_recovereds=self.simulation_params.initial_recovered,
                                  rho=None,
                                  tmin=0,
                                  tmax=self.simulation_params.max_time,
                                  transmission_weight=None,
                                  recovery_weight=None,
                                  return_full_data=True,
                                  )

        elif self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIS and \
                self.simulation_params.algorithm == epidemic_runner.Algorithm.FAST:
            simulation = fast_SIS(self.simulation_params.network,
                                  self.simulation_params.transmission_rate,
                                  self.simulation_params.recovery_rate,
                                  initial_infecteds=self.simulation_params.initial_infected,
                                  rho=None,
                                  tmin=0,
                                  tmax=self.simulation_params.max_time,
                                  transmission_weight=None,
                                  recovery_weight=None,
                                  return_full_data=True,
                                  )

        elif self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIR and \
                self.simulation_params.algorithm == epidemic_runner.Algorithm.DISCRETE:
            simulation = basic_discrete_SIR(G=self.simulation_params.network,
                                            p=self.simulation_params.transmission_probability,
                                            initial_infecteds=self.simulation_params.initial_infected,
                                            initial_recovereds=self.simulation_params.initial_recovered,
                                            rho=None,
                                            tmax=self.simulation_params.max_time,
                                            return_full_data=True
                                            )

        elif self.simulation_params.simulation_type == epidemic_runner.EpidemicSimulationType.SIS and \
                self.simulation_params.algorithm == epidemic_runner.Algorithm.DISCRETE:
            simulation = basic_discrete_SIS(G=self.simulation_params.network,
                                            p=self.simulation_params.transmission_probability,
                                            initial_infecteds=self.simulation_params.initial_infected,
                                            rho=None,
                                            tmax=self.simulation_params.max_time,
                                            return_full_data=True
                                            )

        else:
            raise NotImplementedError

        animation = simulation.animate()

        if save_to_file:
            unique_filename = str(uuid.uuid4())
            animation.save(unique_filename + '.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

        return simulation
