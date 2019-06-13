import networkx as nx

from graphflow.extended.extended_model import ExtendedFlowNetwork, ExtendedFlowNetworkNode, ExtendedFlowNetworkEdge
from ..abstract_simple import abstract_simple_utils


def to_json(network: ExtendedFlowNetwork, indent=None) -> str:
    return abstract_simple_utils.to_json(network, __build_string_network, indent)


def __build_raw_network_from_network(network: ExtendedFlowNetwork) -> nx.DiGraph:
    return abstract_simple_utils.build_raw_network_from_network(network, __build_raw_network)


def __build_raw_network(nodes, edges) -> nx.DiGraph:
    new_network = nx.DiGraph()
    for node in nodes:
        new_network.add_node(node.id, s_flow=node.s_flow)
    for edge in edges:
        new_network.add_edge(edge.u_id, edge.v_id, length=edge.length, cross_area=edge.cross_area,
                             m_flow=edge.m_flow, u_angle=edge.u_angle, v_angle=edge.v_angle,
                             u_pressure=edge.u_pressure, v_pressure=edge.v_pressure)
    return new_network


def __build_string_network(nodes, edges) -> nx.DiGraph:
    new_network = nx.DiGraph()
    for node in nodes:
        new_network.add_node(node.id, s_flow=str(node.s_flow))
    for edge in edges:
        new_network.add_edge(edge.u_id, edge.v_id, length=str(edge.length), cross_area=str(edge.cross_area),
                             m_flow=str(edge.m_flow), u_angle=str(edge.u_angle), v_angle=str(edge.v_angle),
                             u_pressure=str(edge.u_pressure), v_pressure=str(edge.v_pressure))
    return new_network


def from_json(json_network: str) -> ExtendedFlowNetwork:
    return abstract_simple_utils.from_json(json_network, __build_flow_network)


def __build_flow_network(density, raw_network, viscosity):
    flow_network = ExtendedFlowNetwork(density, viscosity)
    for node_id, data in raw_network.nodes(data=True):
        new_node = ExtendedFlowNetworkNode(id=node_id, s_flow=data['s_flow'])
        flow_network.add_node(new_node)
    for u_id, v_id, data in raw_network.edges(data=True):
        new_edge = ExtendedFlowNetworkEdge(u_id=u_id, v_id=v_id, length=data['length'], cross_area=data['cross_area'],
                                           m_flow=data['m_flow'], u_angle=data['u_angle'], v_angle=data['v_angle'],
                                           u_pressure=data['u_pressure'], v_pressure=data['v_pressure'])
        flow_network.add_edge(new_edge)
    return flow_network
