"""contains metrics specific for epidemic networks"""
from sys import maxsize

import networkx as nx
from EoN import estimate_SIR_prob_size
from EoN import Simulation_Investigation


def estimate_SIR_probability(network, trans_prob):
    """returns single float between 0 and 1 estimating probability and proportion of infected"""
    return estimate_SIR_prob_size(network, trans_prob)[0]
    # Uses percolation to estimate the probability
    # and size of epidemics assuming constant transmission probability p


def infected_neighbours(network: nx.Graph, time: float, eon_investigation: Simulation_Investigation):
    """will return dict containing all nodes"""
    statuses = {}
    for n in network.nodes():
        statuses[n] = {'S_neighbours': 0, 'I_neighbours': 0, 'R_neighbours': 0}
        neighbours = network.neighbors(n)
        for nb in neighbours:
            statuses[n][eon_investigation.node_status(nb, time=time)] += 1
    return statuses


def estimate_infection_times(network: nx.Graph, time: float, eon_investigation: Simulation_Investigation):
    # use nx to get all shortest paths, use eon for estimating probability of infection
    estimates = {}
    for n in network.nodes():
        estimates[n] = {'est_inf_time': 0}
        if eon_investigation.node_status(n, time=time) != 'I':
            estimates[n]['est_inf_time'] = maxsize
            statuses = nx.shortest_path_length(network, source=n)
            for k, v in statuses.items():
                if eon_investigation.node_status(k, time=time) == 'I' and v < estimates[n]['est_inf_time']:
                    estimates[n]['est_inf_time'] = v
    return estimates
