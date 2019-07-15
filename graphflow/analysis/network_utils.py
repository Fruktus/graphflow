import csv
from networkx import Graph, DiGraph

from graphflow.models.network import Network
from graphflow.models.simple.simple_model import SimpleFlowNetwork
from graphflow.models.simple.simple_model_utils import __build_string_network as __build_string_network_simple
from graphflow.models.extended.extended_model import ExtendedFlowNetwork
from graphflow.models.extended.extended_model_utils import __build_string_network as __build_string_network_extended
from graphflow.models.epanet.epanet_model import EpanetFlowNetwork


def get_nx_network(network):
    if isinstance(network, SimpleFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_simple(nodes, edges)
    if isinstance(network, ExtendedFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_extended(nodes, edges)
    if isinstance(network, EpanetFlowNetwork):
        return network.get_networkx_graph()
    if isinstance(network, Graph):
        return network
    if isinstance(network, DiGraph):
        return network
    if isinstance(network, Network):
        return network.get_nx_network()
    raise TypeError('unknown network format')


def export_csv(path: str, data: []):
    # data will be array of rows to output
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for row in data:
            if isinstance(row[1], dict):
                writer.writerow(['metrics'] + list(row[1].keys()))
                break
        for row in data:
            if isinstance(row[1], tuple):
                for dictdata in row[1]:
                    writer.writerow([row[0]] + list(dictdata.values()))
            if isinstance(row[1], dict):
                writer.writerow([row[0]] + list(row[1].values()))
            if isinstance(row, int or float):
                continue
