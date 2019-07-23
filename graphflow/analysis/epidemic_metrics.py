"""Metrics for epidemic model. See `graphflow.analysis.metrics.py` for details."""

from sys import maxsize

import networkx as nx
from EoN import estimate_SIR_prob_size, estimate_directed_SIR_prob_size

# TODO change all metrics so that they work according to docstrings, add static/dynamic to each function


def static_estimate_probability(network, **kwargs):
    """
    Estimates of epidemic probability

    **Only SIR**. Same as `static_estimate_attack_rate(network, **kwargs)` for 'discrete' algorithm.

    Args:
        network: networkx graph
        **kwargs: See below

    Keyword Args:
        simulation_type (str): 'sir' or 'sis'. Defaults to 'sir'. 'sis' is illegal and will raise Exception
        algorithm (str): Required. 'fast' or 'discrete'
        transmission_rate (float): Required for **fast**. Transmission rate
        recovery_rate (float): Required for **fast**. Recovery rate
        transmission_probability (float): Required for 'discrete'. Transmission probability. Values between 0 and 1

    Returns:
         float: value between 0 and 1 estimating probability and proportion of infected

    Raises:
        ValueError: Couple of reasons:
            - `simulation_type` is 'sis'
            - Missing arguments for **fast** (`transmission_rate` or `recovery_rate`) or **discrete**
               (`transmission_probability`)

    See Also:
        'graphflow.analysis.metrics'
    """

    simulation_type = kwargs.get('simulation_type', 'sir')
    algorithm = kwargs.get('algorithm', None)
    transmission_rate = kwargs.get('transmission_rate', None)
    recovery_rate = kwargs.get('recovery_rate', None)
    transmission_probability = kwargs.get('transmission_probability', None)

    if simulation_type == 'sis':
        raise ValueError("Metric does not work for 'sis' type")

    if algorithm == 'fast':
        if not transmission_rate:
            raise ValueError("Transmission rate not specified")
        if not recovery_rate:
            raise ValueError("Recovery rate not specified")

        return estimate_directed_SIR_prob_size(network, transmission_rate, recovery_rate)[0]

    elif algorithm == 'discrete':
        if not transmission_probability:
            raise ValueError("Transmission probability not specified")

        return estimate_SIR_prob_size(network, transmission_probability)[0]


def static_estimate_attack_rate(network, **kwargs):
    """
    Calculates attack_rate

    **Only SIR**. Same as `static_estimate_probability(network, **kwargs)` for 'discrete' algorithm.

    Args:
        network: networkx graph
        **kwargs: See below

    Keyword Args:
        simulation_type (str): 'sir' or 'sis'. Defaults to 'sir'. 'sis' is illegal and will raise Exception
        algorithm (str): Required. 'fast' or 'discrete'
        transmission_rate (float): Required for **fast**. Transmission rate
        recovery_rate (float): Required for **fast**. Recovery rate
        transmission_probability (float): Required for 'discrete'. Transmission probability. Values between 0 and 1

    Returns:
         float: value between 0 and 1 estimating probability and proportion of infected

    Raises:
        ValueError: Couple of reasons:
            - `simulation_type` is 'sis'
            - Missing arguments for **fast** (`transmission_rate` or `recovery_rate`) or **discrete**
               (`transmission_probability`)

    See Also:
        'graphflow.analysis.metrics'
    """

    simulation_type = kwargs.get('simulation_type', 'sir')
    algorithm = kwargs.get('algorithm', None)
    transmission_rate = kwargs.get('transmission_rate', None)
    recovery_rate = kwargs.get('recovery_rate', None)
    transmission_probability = kwargs.get('transmission_probability', None)

    if simulation_type == 'sis':
        raise ValueError("Metric does not work for 'sis' type")

    if algorithm == 'fast':
        if not transmission_rate:
            raise ValueError("Transmission rate not specified")
        if not recovery_rate:
            raise ValueError("Recovery rate not specified")

        return estimate_directed_SIR_prob_size(network, transmission_rate, recovery_rate)[1]

    elif algorithm == 'discrete':
        if not transmission_probability:
            raise ValueError("Transmission probability not specified")

        return estimate_SIR_prob_size(network, transmission_probability)[1]


def infected_neighbours(network: nx.Graph, **kwargs):
    """
    Counts infected neighbours for all nodes

    Args:
        network: networkx Graph
        **kwargs: Not used here

    Returns:
        dict: dictionary keyed by nodes id into dict of neighbours counts with given status (S,I,R)

    See Also:
        'graphflow.analysis.metrics'
    """

    status = nx.get_node_attributes(network, 'status')
    infected = {}
    for node in network.nodes():
        infected[node] = 0
        neighbours = network.neighbors(node)  # id's
        for nb in neighbours:
            if status[nb] == 'I':
                infected[node] += 1
    return infected


def estimate_infection_times(network: nx.Graph, **kwargs):
    """Uses average shortest paths to estimate time in steps to infection of given node

        Args:
            network: networkx Graph
            **kwargs: Not used here

        Returns:
            dict: dictionary keyed by nodes id into estimate

        See Also:
            'graphflow.analysis.metrics'
        """

    status = nx.get_node_attributes(network, 'status')

    # use nx to get all shortest paths, use eon for estimating probability of infection
    estimates = {}
    for node in network.nodes():
        estimates[node] = {'est_inf_time': 0}
        if status[node] != 'I':
            estimates[node]['est_inf_time'] = maxsize
            statuses = nx.shortest_path_length(network, source=node)
            for key, value in statuses.items():
                if status[key] == 'I' and value < estimates[node]['est_inf_time']:
                    estimates[node]['est_inf_time'] = value
    return estimates
