# pylint: disable=R0914
from __future__ import annotations

import random
from dataclasses import dataclass, replace
from typing import Optional

import math
import networkx as nx
import numpy as np
import sympy


@dataclass
class ExtendedFlowNetworkNode:
    id: int

    s_flow: Optional[float]


@dataclass
class ExtendedFlowNetworkEdge:
    u_id: int
    v_id: int

    length: float
    cross_area: float
    u_angle: float
    v_angle: float

    m_flow: Optional[float]
    u_pressure: Optional[float]
    v_pressure: Optional[float]


class ExtendedFlowNetwork:
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

    def add_node(self, node: ExtendedFlowNetworkNode):
        self.__internal_network.add_node(node.id)
        self.__internal_nodes[node.id] = node

    def add_edge(self, edge: ExtendedFlowNetworkEdge):
        self.__internal_network.add_edge(edge.u_id, edge.v_id)
        self.__internal_edges[(edge.u_id, edge.v_id)] = edge

    def calculate_network_state(self):
        s_values, m_values = self.__calculate_flow_network_state()
        self.__update_network(s_values, m_values)
        p_in_result, p_out_result = self.__calculate_pressure_network_state()
        return self.__build_new_network(p_in_result, p_out_result)

    # Flow Calculations
    def __calculate_flow_network_state(self):
        s_symbols = {}
        m_symbols = {}
        equations = []

        self.__create_flow_symbols(m_symbols, s_symbols)
        self.__add_initial_flow_conditions(equations, m_symbols, s_symbols)
        self.__add_node_flow_equations(equations, m_symbols, s_symbols)
        s_values, m_values = self.__solve_flow_equations(equations, m_symbols, s_symbols)
        return s_values, m_values

    def __create_flow_symbols(self, m_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            s_symbols[node.id] = sympy.Symbol("s_%i" % node.id)

        for edge in self.__internal_edges.values():
            m_symbols[(edge.u_id, edge.v_id)] = sympy.Symbol('m_%i_%i' % (edge.u_id, edge.v_id))

    def __add_initial_flow_conditions(self, equations, m_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            if node.s_flow is not None:
                equations.append(s_symbols[node.id] - node.s_flow)

        for edge in self.__internal_edges.values():
            if edge.m_flow is not None:
                equations.append(m_symbols[(edge.u_id, edge.v_id)] - edge.m_flow)

    def __add_node_flow_equations(self, equations, m_symbols, s_symbols):
        for node in self.__internal_nodes.values():
            equations.append(self.__build_flow_expr(node, m_symbols, s_symbols))

    def __build_flow_expr(self, node, m_symbols, s_symbols):
        in_edges_m = list(map(lambda x: m_symbols[x], self.__internal_network.in_edges(node.id)))
        out_edges_m = list(map(lambda x: m_symbols[x], self.__internal_network.out_edges(node.id)))
        return s_symbols[node.id] + sum(in_edges_m) - sum(out_edges_m)

    @staticmethod
    def __solve_flow_equations(equations, m_symbols, s_symbols):
        all_symbols = list(s_symbols.values()) + list(m_symbols.values())
        raw_result = sympy.linsolve(equations, all_symbols)
        if not isinstance(raw_result, sympy.FiniteSet):
            raise ValueError()

        result = list(raw_result)[0]
        s_values = result[:len(s_symbols)]
        m_values = result[len(s_symbols):len(s_symbols) + len(m_symbols)]

        s_result = dict(list(zip(s_symbols.keys(), s_values)))
        m_result = dict(list(zip(m_symbols.keys(), m_values)))
        return s_result, m_result

    def __update_network(self, s_values, m_values):
        new_network = ExtendedFlowNetwork(density=self.density, viscosity=self.viscosity)
        for node in self.__internal_nodes.values():
            new_node = replace(node, s_flow=s_values[node.id])
            new_network.add_node(new_node)

        for edge in self.__internal_edges.values():
            if m_values[(edge.u_id, edge.v_id)] >= 0:
                new_edge = replace(edge, m_flow=m_values[(edge.u_id, edge.v_id)])
            else:
                new_edge = replace(edge, u_id=edge.v_id, v_id=edge.u_id, m_flow=-m_values[(edge.u_id, edge.v_id)],
                                   u_angle=edge.v_angle, v_angle=edge.u_angle)
            new_network.add_edge(new_edge)

        self.__internal_network, self.__internal_nodes, self.__internal_edges = new_network.get_internal_components()

    def get_internal_components(self):
        return self.__internal_network, self.__internal_nodes, self.__internal_edges

    # Pressure Calculations
    def __calculate_pressure_network_state(self):
        p_in_symbols = {}
        p_out_symbols = {}
        equations = []

        self.__create_pressure_symbols(p_in_symbols, p_out_symbols)
        self.__add_initial_pressure_conditions(equations, p_in_symbols, p_out_symbols)
        self.__add_pressure_equations(equations, p_in_symbols, p_out_symbols)
        p_in_result, p_out_result = self.__solve_flow_equations(equations, p_in_symbols, p_out_symbols)
        return p_in_result, p_out_result

    def __create_pressure_symbols(self, p_in_symbols, p_out_symbols):
        for edge in self.__internal_edges.values():
            p_in_symbols[(edge.u_id, edge.v_id)] = sympy.Symbol('p_in_%i_%i' % (edge.u_id, edge.v_id))
            p_out_symbols[(edge.v_id, edge.u_id)] = sympy.Symbol('p_out_%i_%i' % (edge.v_id, edge.u_id))

    def __add_initial_pressure_conditions(self, equations, p_in_symbols, p_out_symbols):
        for edge in self.__internal_edges.values():
            if edge.u_pressure is not None:
                equations.append(p_in_symbols[(edge.u_id, edge.v_id)] - edge.u_pressure)

            if edge.v_pressure is not None:
                equations.append(p_out_symbols[(edge.v_id, edge.u_id)] - edge.v_pressure)

    def __add_pressure_equations(self, equations, p_in_symbols, p_out_symbols):
        self.__add_pressure_node_equations(equations, p_in_symbols, p_out_symbols)
        self.__add_pressure_edge_equations(equations, p_in_symbols, p_out_symbols)

    def __add_pressure_node_equations(self, equations, p_in_symbols, p_out_symbols):
        for node in self.__internal_nodes.values():
            in_nodes = [i for (i, j) in self.__internal_network.in_edges(node.id)]
            out_nodes = [j for (i, j) in self.__internal_network.out_edges(node.id)]

            if not in_nodes or not out_nodes:
                continue

            ref = random.choice(in_nodes)

            c_ref = {}
            for j in out_nodes:
                c_ref_j = self.__calculate_coefficients(j, node.id, ref)
                c_ref[(ref, j)] = c_ref_j

                m_node_j = self.__internal_edges[(node.id, j)].m_flow
                a_node_j = self.__internal_edges[(node.id, j)].cross_area
                u_j = m_node_j / (self.density * a_node_j)

                p_in_ref_node = p_in_symbols[(ref, node.id)]
                p_out_j_node = p_out_symbols[(j, node.id)]
                equation = p_in_ref_node - p_out_j_node - c_ref_j * self.density * u_j ** 2
                equations.append(equation)

            m_sum = sum([self.__internal_edges[(node.id, j)].m_flow for j in out_nodes])

            for i in in_nodes:
                if i == ref:
                    continue

                coeff = 0
                for j in out_nodes:
                    c_i_j = self.__calculate_coefficients(j, node.id, ref)

                    m_node_j = self.__internal_edges[(node.id, j)].m_flow
                    a_node_j = self.__internal_edges[(node.id, j)].cross_area
                    u_j = m_node_j / (self.density * a_node_j)
                    coeff += m_node_j / m_sum * (c_i_j - c_ref[(ref, j)]) * self.density * u_j ** 2

                equation = p_out_symbols[(node.id, i)] - p_in_symbols[(ref, node.id)] - coeff
                equations.append(equation)

    def __calculate_coefficients(self, j, node, ref):
        psi = self.__internal_edges[(ref, node)].cross_area / self.__internal_edges[(node, j)].cross_area
        q_ref_j = self.__internal_edges[(node, j)].m_flow / self.__internal_edges[(ref, node)].m_flow
        th_ref_j = (self.__internal_edges[(ref, node)].u_angle - self.__internal_edges[
            (node, j)].u_angle) / math.pi % 1
        c_ref_j = 1 - 1 / (psi * q_ref_j) * math.cos(0.75 * (math.pi - th_ref_j))
        return c_ref_j

    def __add_pressure_edge_equations(self, equations, p_in_symbols, p_out_symbols):
        for edge in self.__internal_edges.values():
            re_val = 2 * edge.m_flow / (self.viscosity * math.sqrt(edge.cross_area) * math.pi)

            f1_val = np.sign(-4.5 * (re_val - 3000) / 1000) * 64 / re_val
            f2_val = np.sign(4.5 * (re_val - 3000) / 1000) * 0.079 / (re_val * 0.25)
            f_val = f1_val + f2_val

            coeff = edge.length * edge.m_flow ** 2 / (self.density * edge.cross_area ** 2) * math.sqrt(
                math.pi / edge.cross_area)
            equation = p_in_symbols[(edge.u_id, edge.v_id)] - p_out_symbols[(edge.v_id, edge.u_id)] - f_val * coeff
            equations.append(equation)

    @staticmethod
    def __solve_pressure_equations(equations, p_in_symbols, p_out_symbols):
        all_symbols = list(p_in_symbols.values()) + list(p_out_symbols.values())
        raw_result = sympy.linsolve(equations, all_symbols)
        if not isinstance(raw_result, sympy.FiniteSet):
            raise ValueError()

        result = list(raw_result)[0]
        p_in_values = result[:len(p_in_symbols)]
        p_out_values = result[len(p_in_symbols):len(p_in_symbols) + len(p_out_symbols)]

        p_in_result = dict(list(zip(p_in_symbols.keys(), p_in_values)))
        p_out_result = dict(list(zip(p_out_symbols.keys(), p_out_values)))
        return p_in_result, p_out_result

    def __build_new_network(self, p_in_symbols, p_out_symbols):
        new_network = ExtendedFlowNetwork(density=self.density, viscosity=self.viscosity)
        for node in self.__internal_nodes.values():
            new_node = replace(node)
            new_network.add_node(new_node)

        for edge in self.__internal_edges.values():
            new_edge = replace(edge, u_pressure=p_in_symbols[(edge.v_id, edge.u_id)],
                               v_pressure=p_out_symbols[(edge.u_id, edge.v_id)])
            new_network.add_edge(new_edge)

        return new_network
