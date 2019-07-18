"""Contains utilities used for calculating networks"""
import networkx as nx

import graphflow.analysis.metrics as mtr
import graphflow.analysis.epidemic_metrics as emtr


def calculate_metric(ntype: str, name: str, network: nx.Graph):
    """Calculates metric given by its string name for specific network type

    Args:
        ntype: the network model to use
        name: metric name
        network: networkx graph

    Returns:
        tuple: contains two fields, first is name, second is the value returned from metric"""
    try:
        if ntype == 'simple':
            return name, getattr(mtr, name)(network)
        if ntype == 'extended':
            return name, getattr(mtr, name)(network)
        if ntype == 'epanet':
            return name, getattr(mtr, name)(network)
        if ntype == 'epidemic':
            if not hasattr(mtr, name):
                return name, getattr(emtr, name)(network)
            return name, getattr(mtr, name)(network)
        raise TypeError('unknown network type')
    except KeyError:
        print('unknown key: ', name)
        return None


def calculate_metric_array(ntype: str, network: nx.Graph, array: [str]):
    """Same as calculate_metric, but can process string array of metrics

    Args:
        ntype: the network model to use
        network: networkx graph
        array: array of metric names to calculate

    Returns:
        array: an array of tuples as in calculate_metric
        """
    arr = []
    for i in array:
        res = calculate_metric(ntype, i, network)
        if res:
            arr.append(res)
    return arr


def apply_metric(ntype, name, network):
    metric = calculate_metric(ntype, name, network)

    if isinstance(metric[1], dict):
        nx.set_node_attributes(network, metric[1], metric[0])
    elif isinstance(metric[1], tuple):
        nx.set_node_attributes(network, metric[1][0], metric[0])
    else:
        network.graph[metric[0]] = metric[1]


def apply_all_metrics(ntype, names: [str], network):
    for metric in names:
        apply_metric(ntype, metric, network)
