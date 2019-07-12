import networkx as nx

import graphflow.analysis.metrics as mtr


def calculate_metric(ntype, name, network):
    """calls available metrics (those in this document)
       returns results (mostly dicts and numerical values"""
    try:
        if ntype == 'simple':
            return name, getattr(mtr, name)(network)
        if ntype == 'extended':
            return name, getattr(mtr, name)(network)
        if ntype == 'epanet':
            return name, getattr(mtr, name)(network)
        if ntype == 'epidemic':
            return name, getattr(mtr, name)(network)
        raise TypeError('unknown network type')
    except KeyError:
        print('unknown key: ', name)
        return None


def calculate_metric_array(ntype: str, network, array: [str]):
    """same as calculate_metric, but processes an array instead of a single metric.
       returns an array containing the results (dicts or values)"""
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
