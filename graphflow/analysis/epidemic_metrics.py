"""contains metrics specific for epidemic networks"""
from sys import maxsize

import networkx as nx
from EoN import estimate_SIR_prob_size
from EoN import Simulation_Investigation


def estimate_sir_size(network, trans_prob):
    """Calculates estimated sir outbreak size
    Args:
        network: networkx graph
        trans_prob: float (0-1), probability of disease spreading further

        Raises:
            ValueError: Network is not calculated

    Returns:
         float: value between 0 and 1 estimating probability and proportion of infected"""
    return estimate_SIR_prob_size(network, trans_prob)[0]
    # Uses percolation to estimate the probability
    # and size of epidemics assuming constant transmission probability p


def infected_neighbours(network: nx.Graph, time: float, eon_investigation: Simulation_Investigation):
    """Counts infected, recovered and susceptible neighbours for all nodes
    Args:
        network: networkx Graph
        time: point in time to calculate metric for
        eon_investigation: object containing history data for all nodes

    Returns:
        dict: dictionary keyed by nodes id into dict of neighbours counts with given status (S,I,R)"""
    statuses = {}
    for node in network.nodes():
        statuses[node] = {'S_neighbours': 0, 'I_neighbours': 0, 'R_neighbours': 0}
        neighbours = network.neighbors(node)
        for nb in neighbours:
            statuses[node][eon_investigation.node_status(nb, time=time)] += 1
    return statuses


def estimate_infection_times(network: nx.Graph, time: float, eon_investigation: Simulation_Investigation):
    """Uses average shortest paths to estimate time in steps to infection of given node
        Args:
            network: networkx Graph
            time: point in time to calculate metric for
            eon_investigation: object containing history data for all nodes

        Returns:
            dict: dictionary keyed by nodes id into estimate"""
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
