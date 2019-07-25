# pylint: skip-file
import pytest
import networkx as nx

from graphflow.analysis.epidemic_metrics import static_attack_rate,\
    static_estimated_infection_time, static_epidemic_probability, dynamic_infected_neighbours


@pytest.fixture(scope='module')
def test_network():
    network = nx.Graph()
    network.add_nodes_from(range(10))
    network.add_edges_from([(0, 1), (1, 2), (1, 3), (1, 5), (2, 6), (2, 7), (7, 8), (2, 9), (3, 9)])
    attr = {0: {'status': 'I'}, 5: {'status': 'I'}}
    nx.set_node_attributes(network, 'S', 'status')
    nx.set_node_attributes(network, attr)
    return network


def test_static_epidemic_probability(test_network, **kwargs):
    res = static_epidemic_probability(test_network, algorithm='discrete',
                                      transmission_probability=0.3)
    assert 0.0 <= res <= 1.0


def test_static_attack_rate(test_network, **kwargs):
    res = static_attack_rate(test_network, algorithm='discrete', transmission_probability=0.3)
    assert 0.0 <= res <= 1.0


def test_static_estimated_infection_time(test_network, **kwargs):
    res = static_estimated_infection_time(test_network)
    assert isinstance(res, dict)


def test_dynamic_infected_neighbours(test_network, **kwargs):
    res = dynamic_infected_neighbours(test_network)
    assert isinstance(res, dict)
