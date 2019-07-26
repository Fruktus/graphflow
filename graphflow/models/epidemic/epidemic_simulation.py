"""
Contains implementation that runs simulation using EoN library functions.

See Also:
    graphflow.models.epidemic.epidemic_network
    https://epidemicsonnetworks.readthedocs.io/en/latest/EoN.html
"""

import uuid
# from EoN import fast_SIR, fast_SIS, basic_discrete_SIR, basic_discrete_SIS
from graphflow.models.epidemic.custom_simulation import fast_SIR, fast_SIS, basic_discrete_SIR, basic_discrete_SIS


# TODO add seed and probability description
from graphflow.models.epidemic.epidemic_runner import ExperimentParameters, EpidemicSimulationType, Algorithm


class Simulation:
    """
    Class that runs epidemic simulation using EoN library functions

    Args:
        sim_params: Simulation parameters
        seed:
        probability:

    See Also:
        graphflow.models.epidemic.epidemic_runner
        graphflow.models.epidemic.epidemic_network
        https://epidemicsonnetworks.readthedocs.io/en/latest/EoN.html
    """
    simulation_params: ExperimentParameters

    def __init__(self, sim_params: ExperimentParameters, seed=None, probability=None):
        self.simulation_params = sim_params
        self.seed = seed
        self.probability = probability
        self.animation = None

    def get_network(self):
        """Returns NetworkX graph on which simulation is ran"""
        return self.simulation_params.network

    def run_simulation(self, save_to_file: bool = False):
        """
        Runs simulation using EoN library functions

        Args:
            save_to_file: If True saves result as mp4 file
        """

        if self.simulation_params.simulation_type == EpidemicSimulationType.SIR and \
                self.simulation_params.algorithm == Algorithm.FAST:
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
                                  seed=self.seed,
                                  probability=self.probability)

        elif self.simulation_params.simulation_type == EpidemicSimulationType.SIS and \
                self.simulation_params.algorithm == Algorithm.FAST:
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

        elif self.simulation_params.simulation_type == EpidemicSimulationType.SIR and \
                self.simulation_params.algorithm == Algorithm.DISCRETE:
            simulation = basic_discrete_SIR(G=self.simulation_params.network,
                                            p=self.simulation_params.transmission_probability,
                                            initial_infecteds=self.simulation_params.initial_infected,
                                            initial_recovereds=self.simulation_params.initial_recovered,
                                            rho=None,
                                            tmax=self.simulation_params.max_time,
                                            return_full_data=True
                                            )

        elif self.simulation_params.simulation_type == EpidemicSimulationType.SIS and \
                self.simulation_params.algorithm == Algorithm.DISCRETE:
            simulation = basic_discrete_SIS(G=self.simulation_params.network,
                                            p=self.simulation_params.transmission_probability,
                                            initial_infecteds=self.simulation_params.initial_infected,
                                            rho=None,
                                            tmax=self.simulation_params.max_time,
                                            return_full_data=True
                                            )

        else:
            raise NotImplementedError

        self.animation = simulation.animate()

        if save_to_file:
            unique_filename = str(uuid.uuid4())
            self.animation.save(unique_filename + '.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

        return simulation
