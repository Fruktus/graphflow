# pylint: skip-file
import webbrowser
from pathlib import Path
import holoviews as hv

from graphflow.models.network import Network
from graphflow.models.simple import simple_model_utils
from graphflow.models.simple.simple_model import SimpleFlowNetwork


class SimpleNetwork(Network):
    """
    SimpleNetwork implements simple model.

    Args:
        path_to_network: path to file containing network in JSON format.
        metrics: used metrics as list of strings. Each name has to be name of one of the functions in on of the
            ``graphflow.analysis.metrics.py`` file
        *args: not used in this model
        **kwargs: not used in this model

    Examples:
        >>> network = SimpleNetwork('network.json', ['degree_centrality', 'diameter'])
        >>> network.calculate()
        >>> network.visualize()
        >>> network.export('exported.csv')
    """

    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'simple'
        self._metrics = metrics

        base_path = Path(__file__).parent.parent.parent
        file_path = (base_path / path_to_network).resolve()

        with open(file_path) as file:
            json_network = file.read()
            self.__network = simple_model_utils.from_json(json_network)

    def get_nx_network(self):
        return simple_flow_network_to_nxnetwork(self.__network)

    def calculate(self):
        new_network = self.__network.calculate_network_state()
        # dict of calculated networks - {time: network}
        self._calculated_networks[0.0] = simple_flow_network_to_nxnetwork(new_network)

        self._is_calculated = True
        self._apply_static_metrics(self._calculated_networks[0.0])
        self._apply_dynamic_metrics(self._calculated_networks[0.0])


def simple_flow_network_to_nxnetwork(network: SimpleFlowNetwork):
    """Converts SimpleFlowNetwork to networkx graph"""
    nodes, edges = network.get_network_state()
    return simple_model_utils.__build_string_network(nodes, edges)
