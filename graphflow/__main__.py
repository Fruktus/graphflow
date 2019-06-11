import argparse
from pathlib import Path

from graphflow.simple.simple_model_analysis import betweenness_centrality, hits, load_centrality
from graphflow.epanet.epanet_model_analysis import current_flow_betweenness
from graphflow.epanet.epanet_model import EpanetFlowNetwork, SimulationType
from graphflow.simple.simple_model_utils import from_json
from graphflow.epanet.epanet_model_vis import get_animation
from graphflow.simple.simple_model_vis import visualize_holoviews


def main():
    parser = argparse.ArgumentParser('python3 -m graphflow')
    subparser = parser.add_subparsers(help='network models', dest='network_model')
    simple_subparser = subparser.add_parser('simple')
    simple_subparser.add_argument('path_to_network_file',
                                  help='path to network file which represents network in json format')
    epanet_subparser = subparser.add_parser('epanet')
    epanet_subparser.add_argument('path_to_network_file',
                                  help='path to network file which represents network in inp format')
    epanet_subparser.add_argument('simulation_type', help='simulation type - pressure, ')
    epanet_subparser.add_argument('--time', help='simulation time in hours', type=int, nargs='?')
    epanet_subparser.add_argument('--trace_node', help='node number that will be observed', nargs='?')
    epidemic_subparser = subparser.add_parser('epidemic')
    epidemic_subparser.add_argument('path_to_network_file',
                                    help='path to network file which represents network in x format')
    args = parser.parse_args()

    if args.network_model == 'simple':
        __sample_routine(args.path_to_network_file)
    elif args.network_model == 'epanet':
        __run_epanet(args)
    elif args.network_model == 'epidemic':
        print("Not implemented yet")


def __sample_routine(graph_filepath):
    base_path = Path(__file__).parent
    file_path = (base_path / graph_filepath).resolve()
    with open(file_path) as file:
        json_network = file.read()
        network = from_json(json_network)

        solved_network = network.calculate_network_state()
        hits_res = hits(solved_network)
        centrality = betweenness_centrality(solved_network)
        load = load_centrality(solved_network)

        print("Authorities: ", hits_res[0])
        print("Hubs: ", hits_res[1])
        print("Centrality: ", centrality)
        print("Load: ", load)
        res = ('bb', betweenness_centrality(solved_network))
        visualize_holoviews(solved_network, [res])


def __run_epanet(args):
    print("Running simulation...")
    if args.simulation_type == 'pressure':
        if not hasattr(args, 'time'):
            raise ValueError('No time range has been passed')
        epanet_flow_network = EpanetFlowNetwork(args.path_to_network_file, SimulationType.PRESSURE, time=args.time)
    elif args.simulation_type == 'quality':
        if not hasattr(args, 'trace_node'):
            raise ValueError('No  trace node has been passed')
        epanet_flow_network = EpanetFlowNetwork(args.path_to_network_file, SimulationType.QUALITY,
                                                trace_node=args.trace_node)
    else:
        raise ValueError('Bad simulation type')

    epanet_flow_network.run_simulation()
    print("Current Flow: ", current_flow_betweenness(epanet_flow_network))
    get_animation(epanet_flow_network, frames=100, fps=1)


if __name__ == '__main__':
    main()
