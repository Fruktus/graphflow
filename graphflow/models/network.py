from abc import ABC, abstractmethod

# def get_network(model: str, path_to_network: str, metrics: [str], *args, **kwargs):
#     if model == 'simple':
#         return SimpleNetwork(path_to_network, metrics, args, kwargs)
#     if model == 'extended':
#         return ExtendedNetwork(path_to_network, metrics, args, kwargs)
#     if model == 'epidemic':
#         return EpidemicNetwork(path_to_network, metrics, args, kwargs)
#     if model == 'epanet':
#         return EpanetNetwork(path_to_network, metrics, args, kwargs)
#
#     raise ValueError("There is no model named: {}".format(model))


class Network(ABC):
    _model: str
    _is_calculated: bool = False
    _metrics: [str] = None
    _calculated_networks = {}

    @property
    def model(self):
        return self._model

    @property
    def metrics(self):
        return self._metrics

    @property
    def is_calculated(self):
        return self._is_calculated

    @abstractmethod
    def get_nx_network(self):
        pass

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def visualize(self):
        pass

    def export(self, path):
        pass
