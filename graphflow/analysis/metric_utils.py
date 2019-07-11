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
