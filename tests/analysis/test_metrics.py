# pylint: skip-file
from pathlib import Path
import pytest

from graphflow.analysis.metrics import *
from graphflow.models.simple.simple_model_utils import from_json
from graphflow.models.simple.simple_network import SimpleNetwork


@pytest.fixture(scope='module')
def test_network():
    network = SimpleNetwork("../examples/simple/example_network.json", None)

    return network.get_nx_network()


def test_degree_centrality(test_network):
    assert isinstance(degree_centrality(test_network), dict)


def test_hits(test_network):
    assert isinstance(hits(test_network), tuple or None)


def test_diameter(test_network):
    assert isinstance(diameter(test_network), int)


def test_density(test_network):
    assert isinstance(density(test_network), float)


# def test_modularity(test_network):
#     assert isinstance(modularity(test_network), None)


def test_page_rank(test_network):
    assert isinstance(page_rank(test_network), dict)


def test_eigenvector_centrality(test_network):
    assert isinstance(eigenvector_centrality(test_network), dict)


def test_closeness_centrality(test_network):
    assert isinstance(closeness_centrality(test_network), dict)


def test_betweenness_centrality(test_network):
    assert isinstance(betweenness_centrality(test_network), dict)


def test_average_path_centrality(test_network):
    assert isinstance(average_path(test_network), float)


# def test_maximum_flow(test_network):
#     assert isinstance(maximum_flow(test_network, source, target),)


def test_current_flow_closeness(test_network):
    assert isinstance(current_flow_closeness(test_network), dict)


def test_current_flow_betweenness(test_network):
    assert isinstance(current_flow_betweenness(test_network), dict)


def test_load_centrality(test_network):
    assert isinstance(load_centrality(test_network), dict)


def test_subgraph(test_network):
    assert isinstance(subgraph(test_network), dict)


def test_harmonic_centrality(test_network):
    assert isinstance(harmonic_centrality(test_network), dict)


def test_global_reaching(test_network):
    assert isinstance(global_reaching(test_network), float)


def test_percolation(test_network):
    assert isinstance(percolation(test_network), dict)


def test_second_order_centrality(test_network):
    assert isinstance(second_order_centrality(test_network), dict)
