# pylint: skip-file
from graphflow.analysis.metric_utils import apply_all_metrics
from graphflow.models.epanet.epanet_model import EpanetFlowNetwork, SimulationType
from graphflow.models.network import Network
from graphflow.models.epanet import epanet_model_vis


class EpanetNetwork(Network):
    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'epanet'
        self._metrics = metrics

        self.__network = EpanetFlowNetwork(path_to_network, args[0], **kwargs)

        self.__network.run_simulation()

    def get_nx_network(self):
        return self.__network.get_networkx_graph()

    # TODO implement
    def calculate(self):
        self.__network.run_simulation()

    # TODO implement
    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        if self._metrics:
            nx_network = self.get_nx_network()
            apply_all_metrics(self._model, nx_network, self._metrics)

            # TODO - holoviews
            # visualize_holoviews(epanet_flow_network, res)

        if self.__network.simulation_type == SimulationType.PRESSURE \
                or self.__network.simulation_type == SimulationType.QUALITY:
            epanet_model_vis.save_animation(self.__network, frames=100, fps=1)
        elif self.__network.simulation_type == SimulationType.EARTHQUAKE:
            epanet_model_vis.draw_epicenter_plot(self.__network)
            epanet_model_vis.draw_fragility_curve_plot(self.__network)
            epanet_model_vis.draw_distance_to_epicenter_plot(self.__network)
            epanet_model_vis.draw_peak_ground_acceleration_plot(self.__network)
            epanet_model_vis.draw_peak_ground_velocity_plot(self.__network)
            epanet_model_vis.draw_repair_rate_plot(self.__network)
            epanet_model_vis.draw_repair_rate_x_pipe_length(self.__network)
            epanet_model_vis.draw_probability_of_minor_leak(self.__network)
            epanet_model_vis.draw_probability_of_major_leak(self.__network)
            epanet_model_vis.draw_damage_states_plot(self.__network)
            epanet_model_vis.show_plots()

    # TODO implement
    def export(self, path):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")
