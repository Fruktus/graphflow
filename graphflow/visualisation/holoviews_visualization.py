import webbrowser

import networkx as nx
import holoviews as hv
from holoviews import opts
from bokeh.io import output_file, show
import EoN

from graphflow.analysis.metric_utils import apply_all_metrics
from graphflow.analysis.network_utils import get_nx_network
from graphflow.models.network import Network


#TODO implement
def get_hv_network(network: Network):
    '''Returns holoviews object from network'''
    pass


#TODO implement
def get_hv_plot(network: Network):
    '''Returns holoviews object from network as HoloMap of curves'''
    pass


#TODO implement
def get_hv_labels(network: Network):
    '''Returns holoviews object from network which acts like a list'''
    pass
