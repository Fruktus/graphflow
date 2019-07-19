"""
Metric utilities contains functions connected with delivering, calculating and applying metrics to networks.

Basically other files in this package connected with metrics shouldn't be used. They just deliver metrics and this
module is responsible for using them.

Attributes:
    METRICS_DICT (dict): Dictionary containing all metrics. {name: (function, model, metric_type)}, where:
        name (str): Metric name
        function (function): Metric as function. See `graphflow.analysis.metrics`
        model (str): Simulation model. Can be one of: 'simple', 'extended', 'epidemic', 'epanet'
        metric_type (str): Metric type. Can be either 'static' or 'dynamic'
        Usage of this attribute is not recommended. Generally it's better to get date through
        `get_metric(name[,details])` function
"""

import inspect

import networkx as nx

import graphflow.analysis.metrics as mtr
import graphflow.analysis.epidemic_metrics as emtr

MODULE_DICT = {'general': mtr, 'epidemic': emtr}

# TODO change how metrics are stored and calculated

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


def metric_list(model: str = 'general', metric_type: str = 'all'):
    """
    Returns list of available metrics

    Each metric is different function in one of the modules:
     - `graphflow.analysis.metrics.py` - contains detailed description of metrics
     - `graphflow.analysis.epidemic_metrics.py`

    Args:
        model: Network model. Can be one of 'simple', 'extended', 'epidemic', 'epanet', 'general' or 'all'. Choosing
            'general' will return metrics available for all models.'
        metric_type: Get only static, dynamic or all metrics. Can be one of: 'static', 'dynamic', 'all'

    Returns:
        [str]: List of strings representing names of metrics

    Raises:
        ValueError: Wrong argument - either ``metric_type`` or ``model``

    See Also:
        graphflow.analysis.metrics.py
    """

    if model == 'general':
        models_to_check = ('general', )
    elif model == 'simple':
        models_to_check = ('simple', )
    elif model == 'extended':
        models_to_check = ('extended', )
    elif model == 'epidemic':
        models_to_check = ('epidemic', )
    elif model == 'epanet':
        models_to_check = ('epanet', )
    elif model == 'all':
        models_to_check = ('general', 'simple', 'extended', 'epidemic', 'epanet')
    else:
        raise ValueError("Unrecognised model: {}".format(model))

    if metric_type == 'static':
        metric_types_to_check = ('static', )
    elif metric_type == 'dynamic':
        metric_types_to_check = ('dynamic', )
    elif metric_type == 'all':
        metric_types_to_check = ('static', 'dynamic')
    else:
        raise ValueError("Wrong metric type: {}. Can be only: 'static', 'dynamic' or 'all'".format(metric_type))

    metrics = []

    for name, (_, other_model, other_type) in METRICS_DICT.items():
        if other_type in metric_types_to_check and other_model in models_to_check:
            metrics.append(name)

    return metrics


def get_metric(name: str, details: bool = False):
    """
    Returns metric (as function) by its name

    Generally better to use than extracting data directly from `metrics_dict`

    Args:
        name: Metric name
        details: Whether to provide more details in addition to function. Defaults to False

    Returns:
        function: Metric as function

        If details = True:
        function, model, metric_type - where:
            function (function): Metric as function
            model (str): Simulation model. Can be one of: 'simple', 'extended', 'epidemic', 'epanet'
            metric_type (str): Metric type. Can be either 'static' or 'dynamic'

    Raises:
        KeyError: When there is no such metric

    See Also:
        graphflow.analysis.metrics
    """
    if details:
        return METRICS_DICT[name]
    return METRICS_DICT[name][0]


def __get_all_metrics_dict():
    """
    Prepares dictionary containing all metrics (as functions) along with their type and model.

    Returns:
        dict: Metric dictionary ``{name: (function, model, metric_type)}``
    """
    prefixes = ('static', 'dynamic')

    return_dict = {}

    for model, module in MODULE_DICT.items():
        names = dir(module)

        for name in names:
            value = getattr(module, name)
            if inspect.isfunction(value):
                splitted = name.split('_', 1)
                if splitted[0] in prefixes:
                    return_dict[splitted[1]] = (value, model, splitted[0])

    return return_dict


METRICS_DICT = __get_all_metrics_dict()
