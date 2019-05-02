import argparse
from pathlib import Path

from graphflow.analysis.simple_model_analysis import degree_centrality, hits
from graphflow.simulation.simple_model_utils import from_json
from graphflow.visualisation.simple_model_vis import visualize


def main():
    parser = argparse.ArgumentParser('python3 -m graphflow')
    parser.add_argument('path_to_network_file', help='path to network file which represents network')
    args = parser.parse_args()
    __sample_routine(args.path_to_network_file)


def __sample_routine(graph_filepath):
    base_path = Path(__file__).parent
    file_path = (base_path / graph_filepath).resolve()
    with open(file_path) as file:
        json_network = file.read()
        network = from_json(json_network)

        solved_network = network.calculate_network_state()
        hits_res = hits(solved_network)
        centrality = degree_centrality(solved_network)

        print("Authorities: ", hits_res[0])
        print("Hubs: ", hits_res[1])
        print("Centrality: ", centrality)
        visualize(solved_network)


if __name__ == '__main__':
    main()
