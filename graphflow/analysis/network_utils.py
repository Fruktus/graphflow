from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_string_network as __build_string_network_simple
from graphflow.extended.extended_model import ExtendedFlowNetwork
from graphflow.extended.extended_model_utils import __build_string_network as __build_string_network_extended
from graphflow.epanet.epanet_model import EpanetFlowNetwork


def get_nx_network(network):
    if isinstance(network, SimpleFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_simple(nodes, edges)
    elif isinstance(network, ExtendedFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_extended(nodes, edges)
    elif isinstance(network, EpanetFlowNetwork):
        return network.get_networkx_graph()
    else:
        raise TypeError('unknown network format')

