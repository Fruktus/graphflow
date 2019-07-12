from graphflow.analysis.metric_utils import apply_all_metrics
from graphflow.analysis.network_utils import export_csv
from graphflow.models.network import Network
from graphflow.models.simple import simple_model_utils
from graphflow.models.simple.simple_model import SimpleFlowNetwork


class SimpleNetwork(Network):
    def __init__(self, path_to_network: str, metrics: [str] = None, *args, **kwargs):
        self._model = 'simple'
        self._metrics = metrics

        with open(path_to_network) as file:
            json_network = file.read()
            self.__network = simple_model_utils.from_json(json_network)

    def get_nx_network(self):
        return simple_flow_network_to_nxnetwork(self.__network)

    def calculate(self):
        new_network = self.__network.calculate_network_state()
        self._calculated_networks[0.0] = simple_flow_network_to_nxnetwork(new_network)

        if self._metrics:
            apply_all_metrics(self._model, self._calculated_networks[0.0], self._metrics)

        self._is_calculated = True

    # TODO implement
    def export(self, path):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        export_csv(path, self._calculated_networks[0.0])

    # TODO implement
    def visualize(self):
        if not self.is_calculated:
            raise ValueError("Network not calculated.")

        # visualize_holoviews(self.__calculated_networks[0.0], res)


def simple_flow_network_to_nxnetwork(network: SimpleFlowNetwork):
    nodes, edges = network.get_network_state()
    return simple_model_utils.__build_string_network(nodes, edges)
