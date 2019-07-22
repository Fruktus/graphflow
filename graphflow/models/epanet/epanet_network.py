# pylint: skip-file
from graphflow.models.epanet.epanet_model import EpanetFlowNetwork, SimulationType
from graphflow.models.network import Network
from graphflow.models.epanet import epanet_model_vis


class EpanetNetwork(Network):
    """
    EpidemicNetwork implements epidemic model, using epanet library. Supports earthquake, pressure and quality
    simulations

    Args:
        path_to_network: Path to file containing network in inp format.
        metrics: Used metrics as list of strings. Each name has to be name of one of the functions in on of the
            ``graphflow.analysis.metrics.py`` file
        *args: Only first one used to specify simulation type
            type (epanet_model.SimulationType): Simulation type. Can be one of: ``EARTHQUAKE``, ``PRESSURE``
            or ``QUALITY``
        **kwargs: Simulation parameters. Different parameters required for different simulation types
            epicenter ((int, int)): Earthquake. Position of earthquake epicenter as tuple of ints
            magnitude (float): Earthquake. Magnitude of earthquake
            depth (int): Earthquake. Depth of earthquake in meters
            time (int): Pressure. Simulation time in hours
            trace_node (int): Quality. Node number that will be observed

        Examples:
            >>> network = EpanetNetwork('network.ipn', ['degree_centrality', 'diameter'], SimulationType.EARTHQUAKE, \
            ... epicenter=(50, 50), magnitude=10.0, depth=args.5)
            >>> network.calculate()
            >>> network.visualize()
            >>> network.export('exported.csv')
    """

    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'epanet'
        self._metrics = metrics

        self.__network = EpanetFlowNetwork(path_to_network, args[0], **kwargs)

        self.__network.run_simulation()

    def get_nx_network(self):
        return self.__network.get_networkx_graph()

    def calculate(self):
        self.__network.run_simulation()

        self._calculated_networks[0.0] = self.get_nx_network()
        if self._metrics:
            apply_all_metrics(self._model, self._calculated_networks[0.0], self._metrics)

        self._is_calculated = True

    def visualize(self):
        """
        Visualizes epanet network

        Works differently for each simulation type:
         - Earthquake: Saves mp4 file
         - Pressure: Shows plots illustrating different parameters
         - Quality: Visualization not supported
        """
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        # TODO - holoviews

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

