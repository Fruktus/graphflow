import json

import networkx as nx

from graphflow.simple.simple_model import SimpleFlowNetwork, SimpleFlowNetworkNode, SimpleFlowNetworkEdge


def to_json(network: SimpleFlowNetwork, indent=None) -> str:
    nodes, edges = network.get_network_state()
    new_network = __build_raw_network(nodes, edges)

    serializable_dict = nx.readwrite.json_graph.node_link_data(new_network)
    serializable_dict['density'] = network.density
    serializable_dict['viscosity'] = network.viscosity
    return json.dumps(serializable_dict, indent=indent)


def __build_raw_network_from_network(network: SimpleFlowNetwork) -> nx.DiGraph:
    nodes, edges = network.get_network_state()
    return __build_raw_network(nodes, edges)


def __build_raw_network(nodes, edges) -> nx.DiGraph:
    new_network = nx.DiGraph()
    for node in nodes:
        new_network.add_node(node.id, pressure=node.pressure, s_flow=node.s_flow)
    for edge in edges:
        new_network.add_edge(edge.u_id, edge.v_id, length=edge.length, cross_area=edge.cross_area, m_flow=edge.m_flow)
    return new_network


def __build_string_network(nodes, edges) -> nx.DiGraph:
    new_network = nx.DiGraph()
    for node in nodes:
        new_network.add_node(node.id, pressure=str(node.pressure), s_flow=str(node.s_flow))
    for edge in edges:
        new_network.add_edge(
            edge.u_id, edge.v_id, length=str(edge.length), cross_area=str(edge.cross_area), m_flow=str(edge.m_flow))
    return new_network


def from_json(json_network: str) -> SimpleFlowNetwork:
    deserializable_dict = json.loads(json_network)
    density = deserializable_dict['density']
    viscosity = deserializable_dict['viscosity']
    raw_network = nx.readwrite.json_graph.node_link_graph(deserializable_dict)

    flow_network = __build_flow_network(density, raw_network, viscosity)
    return flow_network


def __build_flow_network(density, raw_network, viscosity):
    flow_network = SimpleFlowNetwork(density, viscosity)
    for node_id, data in raw_network.nodes(data=True):
        new_node = SimpleFlowNetworkNode(id=node_id, pressure=data['pressure'], s_flow=data['s_flow'])
        flow_network.add_node(new_node)
    for u_id, v_id, data in raw_network.edges(data=True):
        new_edge = SimpleFlowNetworkEdge(u_id=u_id, v_id=v_id, length=data['length'],
                                         cross_area=data['cross_area'], m_flow=data['m_flow'])
        flow_network.add_edge(new_edge)
    return flow_network
