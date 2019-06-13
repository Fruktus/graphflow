from dataclasses import dataclass
from typing import Optional

import networkx as nx


@dataclass
class AbstractFlowNetworkNode:
    id: int

    s_flow: Optional[float]


@dataclass
class AbstractFlowNetworkEdge:
    u_id: int
    v_id: int

    length: float
    cross_area: float
    m_flow: Optional[float]


class AbstractFlowNetwork:
    density: float
    viscosity: float

    _internal_network: nx.DiGraph
    _internal_nodes: dict
    _internal_edges: dict

    def __init__(self, density, viscosity):
        self.density = density
        self.viscosity = viscosity
        self._internal_network = nx.DiGraph()
        self._internal_nodes = {}
        self._internal_edges = {}

    def get_network_state(self) -> (list, list):
        return self._internal_nodes.values(), self._internal_edges.values()

    def add_node(self, node: AbstractFlowNetworkNode):
        self._internal_network.add_node(node.id)
        self._internal_nodes[node.id] = node

    def add_edge(self, edge: AbstractFlowNetworkEdge):
        self._internal_network.add_edge(edge.u_id, edge.v_id)
        self._internal_edges[(edge.u_id, edge.v_id)] = edge
