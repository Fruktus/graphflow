# pylint: skip-file
from pathlib import Path

from graphflow.models.network import Network
from graphflow.models.extended import extended_model_utils
from graphflow.models.extended.extended_model import ExtendedFlowNetwork


class ExtendedNetwork(Network):
    """
    ExtendedNetwork implements extended model.

    Args:
        path_to_network: path to file containing network in JSON format.
        metrics: used metrics as list of strings. Each name has to be name of one of the functions in on of the
            ``graphflow.analysis.metrics`` file
        *args: not used in this model
        **kwargs: not used in this model

    Examples:
        >>> network = ExtendedNetwork('network.json', ['degree_centrality', 'diameter'])
        >>> network.calculate()
        >>> network.visualize()
        >>> network.export('exported.csv')
    """

    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'extended'
        self._metrics = metrics

        base_path = Path(__file__).parent.parent.parent
        file_path = (base_path / path_to_network).resolve()

        with open(file_path) as file:
            json_network = file.read()
            self.__network = extended_model_utils.from_json(json_network)

    def get_nx_network(self):
        return extended_flow_network_to_nxnetwork(self.__network)

    def calculate(self):
        new_network = self.__network.calculate_network_state()
        self._apply_static_metrics(new_network)
        # dict of calculated networks - {time:network}
        self._calculated_networks[0.0] = extended_flow_network_to_nxnetwork(new_network)

        if self._metrics:
            apply_all_metrics(self._model, self._calculated_networks[0.0], self._metrics)

        self._is_calculated = True
        self._apply_dynamic_metrics()


def extended_flow_network_to_nxnetwork(network: ExtendedFlowNetwork):
    """Converts ExtendedFlowNetwork to networkx graph"""
    nodes, edges = network.get_network_state()
    return extended_model_utils.__build_string_network(nodes, edges)
