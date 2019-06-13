from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

import math
import networkx as nx
import sympy
from sympy.solvers.solveset import linsolve


@dataclass
class SimpleFlowNetworkNode:
    id: int

    pressure: Optional[float]
    s_flow: Optional[float]


@dataclass
class SimpleFlowNetworkEdge:
    u_id: int
    v_id: int

    length: float
    cross_area: float
    m_flow: Optional[float]


class SimpleFlowNetwork:
    density: float
    viscosity: float

    __internal_network: nx.DiGraph
    __internal_nodes: dict
    __internal_edges: dict

    def __init__(self, density, viscosity):
        self.density = density
        self.viscosity = viscosity
        self.__internal_network = nx.DiGraph()
        self.__internal_nodes = {}
        self.__internal_edges = {}

    def get_network_state(self) -> (list, list):
        return self.__internal_nodes.values(), self.__internal_edges.values()

    def add_node(self, node: SimpleFlowNetworkNode):
        self.__internal_network.add_node(node.id)
        self.__internal_nodes[node.id] = node

    def add_edge(self, edge: SimpleFlowNetworkEdge):
        self.__internal_network.add_edge(edge.u_id, edge.v_id)
        self.__internal_edges[(edge.u_id, edge.v_id)] = edge

    def calculate_network_state(self) -> Optional[SimpleFlowNetwork]:
        p_symbols = {}
        s_symbols = {}
        m_symbols = {}
        equations = []

        self.__create_symbols(m_symbols, p_symbols, s_symbols)
        self.__add_initial_conditions(equations, m_symbols, p_symbols, s_symbols)
        self.__add_node_equations(equations, m_symbols, p_symbols, s_symbols)
        p_values, s_values, m_values = self.__solve_equations(equations, m_symbols, p_symbols, s_symbols)

        return self.__build_new_network(p_values, s_values, m_values)

    def __create_symbols(self, m_symbols, p_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            p_symbols[node.id] = sympy.Symbol("p_%i" % node.id)
            s_symbols[node.id] = sympy.Symbol("s_%i" % node.id)

        for edge in self.__internal_edges.values():
            m_symbols[(edge.u_id, edge.v_id)] = sympy.Symbol('m_%i_%i' % (edge.u_id, edge.v_id))

    # Initial conditions
    def __add_initial_conditions(self, equations, m_symbols, p_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            self.__add_initial_node_conditions(equations, node, p_symbols, s_symbols)

        for edge in self.__internal_edges.values():
            self.__add_initial_edge_conditions(edge, equations, m_symbols)

    @staticmethod
    def __add_initial_node_conditions(equations, node, p_symbols, s_symbols):
        if node.pressure is not None:
            equations.append(p_symbols[node.id] - node.pressure)
        if node.s_flow is not None:
            equations.append(s_symbols[node.id] - node.s_flow)

    @staticmethod
    def __add_initial_edge_conditions(edge, equations, m_symbols):
        if edge.m_flow is not None:
            equations.append(m_symbols[(edge.u_id, edge.v_id)] - edge.m_flow)

    # Node equations
    def __add_node_equations(self, equations, m_symbols, p_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            equations.append(self.__build_flow_expr(node, m_symbols, s_symbols))

        for edge in self.__internal_edges.values():
            equations.append(self.__build_pressure_expr(edge, m_symbols, p_symbols))

    def __build_flow_expr(self, node, m_symbols, s_symbols):
        in_edges_m = list(map(lambda x: m_symbols[x], self.__internal_network.in_edges(node.id)))
        out_edges_m = list(map(lambda x: m_symbols[x], self.__internal_network.out_edges(node.id)))
        return s_symbols[node.id] + sum(in_edges_m) - sum(out_edges_m)

    def __build_pressure_expr(self, edge, m_symbols, p_symbols):
        p_u = p_symbols[edge.u_id]
        p_v = p_symbols[edge.v_id]
        m_u_v = m_symbols[(edge.u_id, edge.v_id)]

        coefficient = 8 * (self.viscosity * math.pi / self.density) * (edge.length / edge.cross_area ** 2)
        return p_u - p_v - coefficient * m_u_v

    @staticmethod
    def __solve_equations(equations, m_symbols, p_symbols, s_symbols):
        all_symbols = list(p_symbols.values()) + list(s_symbols.values()) + list(m_symbols.values())
        raw_result = linsolve(equations, all_symbols)
        if not isinstance(raw_result, sympy.FiniteSet):
            raise ValueError()

        result = list(raw_result)[0]
        p_values = result[:len(p_symbols)]
        s_values = result[len(p_symbols):len(p_symbols) + len(s_symbols)]
        m_values = result[len(p_symbols) + len(s_symbols):len(p_symbols) + len(s_symbols) + len(m_symbols)]

        p_result = dict(list(zip(p_symbols.keys(), p_values)))
        s_result = dict(list(zip(s_symbols.keys(), s_values)))
        m_result = dict(list(zip(m_symbols.keys(), m_values)))
        return p_result, s_result, m_result

    def __build_new_network(self, p_values, s_values, m_values):
        new_network = SimpleFlowNetwork(density=self.density, viscosity=self.viscosity)
        for node in self.__internal_nodes.values():
            new_node = replace(node, pressure=p_values[node.id], s_flow=s_values[node.id])
            new_network.add_node(new_node)

        for edge in self.__internal_edges.values():
            if m_values[(edge.u_id, edge.v_id)] >= 0:
                new_edge = replace(edge, m_flow=m_values[(edge.u_id, edge.v_id)])
            else:
                new_edge = replace(edge, u_id=edge.v_id, v_id=edge.u_id, m_flow=-m_values[(edge.u_id, edge.v_id)])
            new_network.add_edge(new_edge)
        return new_network
