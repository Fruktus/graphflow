# pylint: skip-file
import pytest

from graphflow.analysis.metrics import *
from graphflow.models.simple.simple_network import SimpleNetwork


@pytest.fixture(scope='module')
def test_network():
    network = SimpleNetwork('../examples/simple/example_network.json', None)

    return network.get_nx_network()


def test_degree_centrality(test_network):
    assert isinstance(static_degree_centrality(test_network), dict)


def test_hits(test_network):
    assert isinstance(static_hits(test_network), tuple or None)


def test_diameter(test_network):
    assert isinstance(static_diameter(test_network), int)


def test_density(test_network):
    assert isinstance(static_density(test_network), float)


# def test_modularity(test_network):
#     assert isinstance(modularity(test_network), None)


def test_page_rank(test_network):
    assert isinstance(static_page_rank(test_network), dict)


def test_eigenvector_centrality(test_network):
    assert isinstance(static_eigenvector_centrality(test_network), dict)


def test_closeness_centrality(test_network):
    assert isinstance(static_closeness_centrality(test_network), dict)


def test_betweenness_centrality(test_network):
    assert isinstance(static_betweenness_centrality(test_network), dict)


def test_average_path_centrality(test_network):
    assert isinstance(static_average_path(test_network), float)


# def test_maximum_flow(test_network):
#     assert isinstance(maximum_flow(test_network, source, target),)


def test_current_flow_closeness(test_network):
    assert isinstance(static_current_flow_closeness(test_network), dict)


def test_current_flow_betweenness(test_network):
    assert isinstance(static_current_flow_betweenness(test_network), dict)


def test_load_centrality(test_network):
    assert isinstance(static_load_centrality(test_network), dict)


def test_subgraph(test_network):
    assert isinstance(static_subgraph(test_network), dict)


def test_harmonic_centrality(test_network):
    assert isinstance(static_harmonic_centrality(test_network), dict)


def test_global_reaching(test_network):
    assert isinstance(static_global_reaching(test_network), float)


def test_percolation(test_network):
    assert isinstance(static_percolation(test_network), dict)


def test_second_order_centrality(test_network):
    assert isinstance(static_second_order_centrality(test_network), dict)
