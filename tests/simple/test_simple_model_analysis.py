# pylint: disable=R0801,W0401,W0614
from pathlib import Path
import pytest

from graphflow.simple.simple_model_analysis import *
from graphflow.simple.simple_model_utils import from_json


@pytest.fixture(scope='module')
def test_network():
    base_path = Path(__file__).parent.parent.parent
    file_path = (base_path / "examples" / "simple" / "example_network.json").resolve()
    with open(file_path) as file:
        json_network = file.read()
        network = from_json(json_network)
        net = network.calculate_network_state()
    return net


def test_degree_centrality(net):
    assert isinstance(degree_centrality(net), dict)


def test_hits(net):
    assert isinstance(hits(net), tuple or None)


def test_diameter(net):
    assert isinstance(diameter(net), int)


def test_density(net):
    assert isinstance(density(net), float)


# def test_modularity(net):
#     assert isinstance(modularity(net), None)


def test_page_rank(net):
    assert isinstance(page_rank(net), dict)


def test_eigenvector_centrality(net):
    assert isinstance(eigenvector_centrality(net), dict)


def test_closeness_centrality(net):
    assert isinstance(closeness_centrality(net), dict)


def test_betweenness_centrality(net):
    assert isinstance(betweenness_centrality(net), dict)


def test_average_path_centrality(net):
    assert isinstance(average_path(net), float)


# def test_maximum_flow(net):
#     assert isinstance(maximum_flow(net, source, target),)


def test_current_flow_closeness(net):
    assert isinstance(current_flow_closeness(net), dict)


def test_current_flow_betweenness(net):
    assert isinstance(current_flow_betweenness(net), dict)


def test_load_centrality(net):
    assert isinstance(load_centrality(net), dict)


def test_subgraph(net):
    assert isinstance(subgraph(net), dict)


def test_harmonic_centrality(net):
    assert isinstance(harmonic_centrality(net), dict)


def test_global_reaching(net):
    assert isinstance(global_reaching(net), float)


def test_percolation(net):
    assert isinstance(percolation(net), dict)


def test_second_order_centrality(net):
    assert isinstance(second_order_centrality(net), dict)
