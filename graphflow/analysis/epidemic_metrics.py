"""Metrics for epidemic model. See `graphflow.analysis.metrics` for details."""
from sys import maxsize

import networkx as nx
from EoN import estimate_SIR_prob_size


def estimate_sir_size(network, **kwargs):
    """
    Calculates estimated sir outbreak size
    Args:
        network: networkx graph
        **kwargs: See below

        Raises:
            ValueError: Network is not calculated

    Keyword Args:
        trans_prob: float (0-1), probability of disease spreading further

    Returns:
         float: value between 0 and 1 estimating probability and proportion of infected

    See Also:
        'graphflow.analysis.metrics'
    """

    trans_prob = kwargs.get('trans_prob', 0.5)

    return estimate_SIR_prob_size(network, trans_prob)[0]
    # Uses percolation to estimate the probability
    # and size of epidemics assuming constant transmission probability p


# def infected_neighbours(network: nx.Graph, time: float, eon_investigation: Simulation_Investigation):
#     """Counts infected, recovered and susceptible neighbours for all nodes
#     Args:
#         network: networkx Graph
#         time: point in time to calculate metric for
#         eon_investigation: object containing history data for all nodes
#
#     Returns:
#         dict: dictionary keyed by nodes id into dict of neighbours counts with given status (S,I,R)"""
#     statuses = {}
#     for node in network.nodes():
#         statuses[node] = {'S_neighbours': 0, 'I_neighbours': 0, 'R_neighbours': 0}
#         neighbours = network.neighbors(node)  # id's
#         for nb in neighbours:
#             statuses[node][eon_investigation.node_status(nb, time=time)] += 1
#     return statuses

def infected_neighbours(network: nx.Graph, **kwargs):
    """
    Counts infected, recovered and susceptible neighbours for all nodes
    Args:
        network: networkx Graph
        **kwargs: See below

    Keyword Args:
        state (dict): Required if `network` doesn't have 'state' for each node. See: 'graphflow.analysis.metrics'

    Returns:
        dict: dictionary keyed by nodes id into dict of neighbours counts with given status (S,I,R)

    See Also:
        'graphflow.analysis.metrics'
    """

    statuses = {}
    for node in network.nodes():
        statuses[node] = {'S': 0, 'I': 0, 'R': 0}
        neighbours = network.neighbors(node)  # id's
        status = nx.get_node_attributes(network, 'status')
        for nb in neighbours:
            statuses[node][status[nb]] += 1
        statuses[node]['S_neighbours'] = statuses[node].pop('S')
        statuses[node]['I_neighbours'] = statuses[node].pop('I')
        statuses[node]['R_neighbours'] = statuses[node].pop('R')
    return statuses


def estimate_infection_times(network: nx.Graph, **kwargs):
    """Uses average shortest paths to estimate time in steps to infection of given node
        Args:
            network: networkx Graph
            **kwargs: See below

        Keyword Args:
            time: point in time to calculate metric for
            eon_investigation: object containing history data for all nodes

        Returns:
            dict: dictionary keyed by nodes id into estimate

        See Also:
            'graphflow.analysis.metrics'
        """
    time = kwargs.get('time')
    eon_investigation = kwargs.get('eon_investigation')

    # use nx to get all shortest paths, use eon for estimating probability of infection
    estimates = {}
    for node in network.nodes():
        estimates[node] = {'est_inf_time': 0}
        if eon_investigation.node_status(node, time=time) != 'I':
            estimates[node]['est_inf_time'] = maxsize
            statuses = nx.shortest_path_length(network, source=node)
            for key, value in statuses.items():
                if eon_investigation.node_status(key, time=time) == 'I' and value < estimates[node]['est_inf_time']:
                    estimates[node]['est_inf_time'] = value
    return estimates
