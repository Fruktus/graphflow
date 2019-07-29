import argparse
import os
import sys
import logging

from pathlib import Path

from graphflow.models.epanet.epanet_model import SimulationType
from graphflow.models.epanet.epanet_network import EpanetNetwork
from graphflow.models.epidemic.epidemic_network import EpidemicNetwork
from graphflow.models.extended.extended_network import ExtendedNetwork
from graphflow.models.simple.simple_network import SimpleNetwork

from graphflow.visualisation.gui import Gui


def main():
    logging.basicConfig(level=logging.INFO, format='{asctime} {name:<10} {levelname:10s} {message}', style='{')
    parser = argparse.ArgumentParser('python3 -m graphflow', fromfile_prefix_chars='@')
    subparser = parser.add_subparsers(help='network models', dest='network_model')

    simple_subparser = subparser.add_parser('simple')
    simple_subparser.add_argument('path_to_network_file',
                                  help='path to network file which represents network in json format')
    simple_subparser.add_argument('--metric', '-m', action='append',
                                  help='metric to use, can be specified multiple times')
    simple_subparser.add_argument('--visualize', action='store_true', default=False,
                                  help='whether to visualize results')

    extended_subparser = subparser.add_parser('extended')
    extended_subparser.add_argument('path_to_network_file',
                                    help='path to network file which represents network in json format')
    extended_subparser.add_argument('--metric', '-m', action='append',
                                    help='metric to use, can be specified multiple times')
    extended_subparser.add_argument('--visualize', action='store_true', default=False,
                                    help='whether to visualize results')

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
    epanet_subparser.add_argument('--metric', '-m', action='append',
                                  help='metric to use, can be specified multiple times')
    epanet_subparser.add_argument('--visualize', action='store_true', default=False,
                                  help='whether to visualize results')

    epidemic_subparser = subparser.add_parser('epidemic')
    epidemic_subparser.add_argument('path_to_network_file',
                                    help='path to network file which represents network in gml format')
    epidemic_subparser.add_argument('simulation_type', help='simulation type - sir or sis')
    epidemic_subparser.add_argument('algorithm', help='Algorithm to use - fast or discrete')
    epidemic_subparser.add_argument('--transmission_rate', help='transmission rate', type=float, default=2.0)
    epidemic_subparser.add_argument('--recovery_rate', help='recovery rate', type=float, default=1.0)
    epidemic_subparser.add_argument('--transmission_probability', help='transmission_probability',
                                    type=float, default=0.2)
    epidemic_subparser.add_argument('--max_time', '-t', help='max simulation time, ', type=float, default=2.0)
    epidemic_subparser.add_argument('--time_step_length', help='Length of time step', type=float, default=None)
    epidemic_subparser.add_argument('--metric', '-m', action='append',
                                    help='metric to use, can be specified multiple times')
    epidemic_subparser.add_argument('--visualize', type=str, default='none',
                                    help="visualization of results. Can be: 'none', 'holoviews' or 'mp4'")
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        Gui().start()
        sys.exit()

    base_path = Path(__file__).parent
    os.chdir(base_path)

    if args.network_model == 'simple':
        __run_simple(args)
    elif args.network_model == 'extended':
        __run_extended(args)
    elif args.network_model == 'epanet':
        __run_epanet(args)
    elif args.network_model == 'epidemic':
        __run_epidemic(args)


def __run_simple(args):

    network = SimpleNetwork(args.path_to_network_file, args.metric)

    network.calculate()

    if args.visualize:
        network.visualize()


def __run_extended(args):

    network = ExtendedNetwork(args.path_to_network_file, args.metric)

    network.calculate()

    if args.visualize:
        network.visualize()


def __run_epanet(args):

    if args.simulation_type == 'earthquake':
        if not (args.epicenter_x
                and args.epicenter_y
                and args.magnitude
                and args.depth):
            raise ValueError('No all arguments have been passed')
        network = EpanetNetwork(args.path_to_network_file, args.metric, SimulationType.EARTHQUAKE,
                                epicenter=(args.epicenter_x, args.epicenter_y),
                                magnitude=args.magnitude,
                                depth=args.depth)

    elif args.simulation_type == 'pressure':
        if not hasattr(args, 'time'):
            raise ValueError('No time range has been passed')
        network = EpanetNetwork(args.path_to_network_file, args.metric, SimulationType.PRESSURE,
                                time=args.time)

    elif args.simulation_type == 'quality':
        if not hasattr(args, 'trace_node'):
            raise ValueError('No  trace node has been passed')
        network = EpanetNetwork(args.path_to_network_file, args.metric, SimulationType.QUALITY,
                                trace_node=args.trace_node)

    else:
        raise ValueError('Bad simulation type')

    network.calculate()

    if args.visualize:
        network.visualize()


def __run_epidemic(args):

    network = EpidemicNetwork(args.path_to_network_file, args.metric,
                              simulation_type=args.simulation_type,
                              algorithm=args.algorithm,
                              transmission_rate=args.transmission_rate,
                              recovery_rate=args.recovery_rate,
                              transmission_probability=args.transmission_probability,
                              max_time=args.max_time,
                              time_step_length=args.time_step_length)

    network.calculate()

    if args.visualize != 'none':
        network.visualize(vis_type=args.visualize)

if __name__ == '__main__':
    main()
