from graphflow.analysis.metric_utils import apply_all_metrics
from graphflow.models.extended.extended_model_utils import to_json as extended_to_json
from graphflow.models.network import Network
from graphflow.models.extended import extended_model_utils
from graphflow.models.extended.extended_model import ExtendedFlowNetwork


class ExtendedNetwork(Network):

    def __init__(self, path_to_network: str, metrics: [str], *args, **kwargs):
        self._model = 'extended'
        self._metrics = metrics

        with open(path_to_network) as file:
            json_network = file.read()
            self.__network = extended_model_utils.from_json(json_network)

    def get_nx_network(self):
        return extended_flow_network_to_nxnetwork(self.__network)

    def calculate(self):
        new_network = self.__network.calculate_network_state()
        self._calculated_networks[0.0] = extended_flow_network_to_nxnetwork(new_network)

        if self._metrics:
            apply_all_metrics(self._model, self._calculated_networks[0.0], self._metrics)

        self._is_calculated = True

    # TODO implement
    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

    # TODO implement
    def export(self, path):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        # possible other formats than csv maybe ?
        solved_network = self.__network.calculate_network_state()
        json = extended_to_json(solved_network)


def extended_flow_network_to_nxnetwork(network: ExtendedFlowNetwork):
    nodes, edges = network.get_network_state()
    return extended_model_utils.__build_string_network(nodes, edges)