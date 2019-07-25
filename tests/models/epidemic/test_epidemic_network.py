# pylint: skip-file
import pytest
from os.path import abspath, dirname, join
from networkx import Graph
from EoN import FuncAnimation

from graphflow.models.epidemic.epidemic_network import EpidemicNetwork


@pytest.fixture(scope='module')
def test_network() -> EpidemicNetwork:
    path = join(dirname(dirname(dirname(dirname(abspath(__file__))))), 'examples', 'epidemic', 'karate_graph.gml')
    return EpidemicNetwork(path, None, simulation_type='sir', algorithm='discrete',
                           transmission_probability=0.3, max_time=20)


def test_get_nx_network(test_network):
    assert isinstance(test_network.get_nx_network(), Graph)


def test_calculate(test_network):
    test_network.calculate()
    assert test_network.is_calculated


def test_animate(test_network):
    assert isinstance(test_network.animate(), FuncAnimation)
