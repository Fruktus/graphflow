# pylint: skip-file
from pathlib import Path
import pytest

from graphflow.analysis.network_utils import get_nx_network
from graphflow.simple.simple_model_utils import from_json
from networkx import DiGraph
from networkx import Graph


@pytest.fixture(scope='module')
def test_network():
    base_path = Path(__file__).parent.parent.parent
    file_path = (base_path / "examples" / "simple" / "example_network.json").resolve()
    with open(file_path) as file:
        json_network = file.read()
        network = from_json(json_network)
        test_network = network.calculate_network_state()
    return test_network


def test_get_ns_network(test_network):
    nxnet = get_nx_network(test_network)
    assert isinstance(nxnet, DiGraph or Graph)
