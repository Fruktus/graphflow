from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

import math
import sympy
from sympy.solvers.solveset import linsolve

from graphflow.models.abstract_simple.abstract_simple_model import AbstractFlowNetwork, AbstractFlowNetworkNode, \
    AbstractFlowNetworkEdge


@dataclass
class SimpleFlowNetworkNode(AbstractFlowNetworkNode):
    pressure: Optional[float]


@dataclass
class SimpleFlowNetworkEdge(AbstractFlowNetworkEdge):
    pass


class SimpleFlowNetwork(AbstractFlowNetwork):

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
        for node in self._internal_nodes.values():
            p_symbols[node.id] = sympy.Symbol("p_%i" % node.id)
            s_symbols[node.id] = sympy.Symbol("s_%i" % node.id)

        for edge in self._internal_edges.values():
            m_symbols[(edge.u_id, edge.v_id)] = sympy.Symbol('m_%i_%i' % (edge.u_id, edge.v_id))

    # Initial conditions
    def __add_initial_conditions(self, equations, m_symbols, p_symbols, s_symbols):
        for node in self._internal_nodes.values():
            self.__add_initial_node_conditions(equations, node, p_symbols, s_symbols)

        for edge in self._internal_edges.values():
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
        for node in self._internal_nodes.values():
            equations.append(self.__build_flow_expr(node, m_symbols, s_symbols))

        for edge in self._internal_edges.values():
            equations.append(self.__build_pressure_expr(edge, m_symbols, p_symbols))

    def __build_flow_expr(self, node, m_symbols, s_symbols):
        in_edges_m = list(map(lambda x: m_symbols[x], self._internal_network.in_edges(node.id)))
        out_edges_m = list(map(lambda x: m_symbols[x], self._internal_network.out_edges(node.id)))
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
        self.__fill_with_nodes(new_network, p_values, s_values)
        self.__fill_with_edges(m_values, new_network)
        return new_network

    def __fill_with_nodes(self, new_network, p_values, s_values):
        for node in self._internal_nodes.values():
            new_node = replace(node, pressure=p_values[node.id], s_flow=s_values[node.id])
            new_network.add_node(new_node)

    def __fill_with_edges(self, m_values, new_network):
        for edge in self._internal_edges.values():
            if m_values[(edge.u_id, edge.v_id)] >= 0:
                new_edge = replace(edge, m_flow=m_values[(edge.u_id, edge.v_id)])
            else:
                new_edge = replace(edge, u_id=edge.v_id, v_id=edge.u_id, m_flow=-m_values[(edge.u_id, edge.v_id)])
            new_network.add_edge(new_edge)
