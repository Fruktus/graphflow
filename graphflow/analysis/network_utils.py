import csv
from graphflow.simple.simple_model import SimpleFlowNetwork
from graphflow.simple.simple_model_utils import __build_string_network as __build_string_network_simple
from graphflow.extended.extended_model import ExtendedFlowNetwork
from graphflow.extended.extended_model_utils import __build_string_network as __build_string_network_extended
from graphflow.epanet.epanet_model import EpanetFlowNetwork
from networkx import Graph, DiGraph


def get_nx_network(network):
    if isinstance(network, SimpleFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_simple(nodes, edges)
    elif isinstance(network, ExtendedFlowNetwork):
        nodes, edges = network.get_network_state()
        return __build_string_network_extended(nodes, edges)
    elif isinstance(network, EpanetFlowNetwork):
        return network.get_networkx_graph()
    elif isinstance(network, Graph):
        return network
    elif isinstance(network, DiGraph):
        return network
    else:
        raise TypeError('unknown network format')


def export_csv(data: [], path: str):
    # data will be array of rows to output
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for r in data:
            if isinstance(r[1], dict):
                writer.writerow(['metrics'] + list(r[1].keys()))
                break
        for r in data:
            print('csv:', r)
            if isinstance(r[1], tuple):
                for dictdata in r[1]:
                    writer.writerow([r[0]] + list(dictdata.values()))
            if isinstance(r[1], dict):
                    writer.writerow([r[0]] + list(r[1].values()))
            if isinstance(r, int or float):
                continue
