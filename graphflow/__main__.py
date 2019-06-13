import argparse
from pathlib import Path

from graphflow.epanet.epanet_model import EpanetFlowNetwork, SimulationType
from graphflow.epanet.epanet_model_vis import get_animation
from graphflow.epanet.epanet_model_vis import show_plots, draw_epicenter_plot, draw_fragility_curve_plot, \
    draw_distance_to_epicenter_plot, draw_peak_ground_acceleration_plot, draw_peak_ground_velocity_plot, \
    draw_repair_rate_plot, draw_repair_rate_x_pipe_length, draw_probability_of_minor_leak, \
    draw_probability_of_major_leak, draw_damage_states_plot
from graphflow.epidemic.epidemic_runner import Parser
from graphflow.epidemic.epidemic_simulation import Simulation
from graphflow.extended.extended_model_utils import from_json as extended_from_json
from graphflow.extended.extended_model_utils import to_json as extended_to_json
from graphflow.simple.simple_model_analysis import betweenness_centrality, load_centrality
from graphflow.simple.simple_model_analysis import hits
from graphflow.simple.simple_model_utils import from_json
from graphflow.simple.simple_model_vis import visualize_holoviews


def main():
    parser = argparse.ArgumentParser('python3 -m graphflow')
    subparser = parser.add_subparsers(help='network models', dest='network_model')

    simple_subparser = subparser.add_parser('simple')
    simple_subparser.add_argument('path_to_network_file',
                                  help='path to network file which represents network in json format')

    extended_subparser = subparser.add_parser('extended')
    extended_subparser.add_argument('path_to_network_file',
                                    help='path to network file which represents network in json format')

    epanet_subparser = subparser.add_parser('epanet')
    epanet_subparser.add_argument('path_to_network_file',
                                  help='path to network file which represents network in inp format')
    epanet_subparser.add_argument('simulation_type', help='simulation type - pressure or earthquake, ')
    epanet_subparser.add_argument('--time', help='simulation time in hours', type=int, nargs='?')
    epanet_subparser.add_argument('--trace_node', help='node number that will be observed', nargs='?')
    epanet_subparser.add_argument('--epicenter_x', help='x cord of earthquake epicenter', type=int, nargs='?')
    epanet_subparser.add_argument('--epicenter_y', help='y cord of earthquake epicenter', type=int, nargs='?')
    epanet_subparser.add_argument('--magnitude', help='magnitude of earthquake ', type=float, nargs='?')
    epanet_subparser.add_argument('--depth', help='depth of earthquake in meters', type=int, nargs='?')

    epidemic_subparser = subparser.add_parser('epidemic')
    epidemic_subparser.add_argument('path_to_network_file',
                                    help='path to network file which represents network in x format')
    args = parser.parse_args()

    if args.network_model == 'simple':
        __sample_routine(args.path_to_network_file)
    elif args.network_model == 'extended':
        __sample_routine_two(args.path_to_network_file)
    elif args.network_model == 'epanet':
        __run_epanet(args)
    elif args.network_model == 'epidemic':
        __run_epidemic(args)


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


def __sample_routine_two(graph_filepath):
    base_path = Path(__file__).parent
    file_path = (base_path / graph_filepath).resolve()
    with open(file_path) as file:
        json_network = file.read()
        network = extended_from_json(json_network)
        solved_network = network.calculate_network_state()
        json = extended_to_json(solved_network)
        print(json)


def __run_epanet(args):
    print("Running simulation...")
    if args.simulation_type == 'earthquake':
        if not (hasattr(args, 'epicenter_x')
                and hasattr(args, 'epicenter_y')
                and hasattr(args, 'magnitude')
                and hasattr(args, 'depth')):
            raise ValueError('No all arguments have been passed')
        epanet_flow_network = EpanetFlowNetwork(args.path_to_network_file, SimulationType.EARTHQUAKE,
                                                epicenter=(args.epicenter_x, args.epicenter_y),
                                                magnitude=args.magnitude,
                                                depth=args.depth)
    elif args.simulation_type == 'pressure':
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

    if args.simulation_type == 'pressure' or args.simulation_type == 'quality':
        get_animation(epanet_flow_network, frames=100, fps=1)
    elif args.simulation_type == 'earthquake':
        draw_epicenter_plot(epanet_flow_network)
        draw_fragility_curve_plot(epanet_flow_network)
        draw_distance_to_epicenter_plot(epanet_flow_network)
        draw_peak_ground_acceleration_plot(epanet_flow_network)
        draw_peak_ground_velocity_plot(epanet_flow_network)
        draw_repair_rate_plot(epanet_flow_network)
        draw_repair_rate_x_pipe_length(epanet_flow_network)
        draw_probability_of_minor_leak(epanet_flow_network)
        draw_probability_of_major_leak(epanet_flow_network)
        draw_damage_states_plot(epanet_flow_network)
        show_plots()


def __run_epidemic(args):
    epidemic_params = Parser()
    epidemic_params.parse_input(args.type, args.path_to_network_file, args.transrate, args.recrate, args.tmax)
    simulation_config = epidemic_params.get_simulation_config()

    my_sim = Simulation(simulation_config)
    my_sim.run_simulation()


if __name__ == '__main__':
    main()
