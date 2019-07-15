import json

import networkx as nx

from .abstract_simple_model import AbstractFlowNetwork


def to_json(network: AbstractFlowNetwork, serialize_model, indent=None):
    nodes, edges = network.get_network_state()
    new_network = serialize_model(nodes, edges)

    serializable_dict = nx.readwrite.json_graph.node_link_data(new_network)
    serializable_dict['density'] = network.density
    serializable_dict['viscosity'] = network.viscosity
    return json.dumps(serializable_dict, indent=indent)


def from_json(json_network: str, network_builder):
    deserializable_dict = json.loads(json_network)
    density = deserializable_dict['density']
    viscosity = deserializable_dict['viscosity']
    raw_network = nx.readwrite.json_graph.node_link_graph(deserializable_dict)

    flow_network = network_builder(density, raw_network, viscosity)
    return flow_network


def build_raw_network_from_network(network: AbstractFlowNetwork, network_builder) -> nx.DiGraph:
    nodes, edges = network.get_network_state()
    return network_builder(nodes, edges)
