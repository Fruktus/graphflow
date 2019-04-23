import argparse
from .simulate import simulate_graph_flow


def main():
    parser = argparse.ArgumentParser('python3 -m gf')
    parser.add_argument('path_to_graph_file', help='path to graph file which represents network')
    args = parser.parse_args()
    simulate_graph_flow(args.path_to_graph_file)


if __name__ == '__main__':
    main()
