# pylint: disable=redefined-outer-name
import json
from pathlib import Path

import pytest
from jsondiff import diff

from graphflow.models.simple.simple_model_utils import from_json, to_json


def test_back_and_forth_conversion(network_json):
    network_from_json = from_json(network_json)
    network_as_json = to_json(network_from_json)

    json_1 = json.loads(network_json)
    json_2 = json.loads(network_as_json)
    difference = diff(json_1, json_2)
    assert difference == json.loads('{}')


@pytest.fixture(scope='module')
def network_json() -> str:
    base_path = Path(__file__).parent
    file_path = (base_path / '../../examples/simple/example_network.json').resolve()
    with open(file_path) as file:
        json_network = file.read()
    return json_network
