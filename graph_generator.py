# pylint: skip-file
import networkx as nx
import matplotlib.pyplot as plt
import argparse


def main():
    path = 'examples/generated_graphs'

    # -------------------------------------------
    function = nx.random_powerlaw_tree_sequence
    args = [50]
    infected_nodes = [0, 1, 2]
    save = 0
    # -------------------------------------------

    G = function(*args)
    def map_fun(x):
        if isinstance(x, int):
            return str(x)
        if isinstance(x, float):
            return str(int(x)) + '-' + str(int((x - int(x)) * 100))
        return ''
    filename = function.__name__ + '_' + '_'.join(map(map_fun, args)) + '.gml'

    nx.set_node_attributes(G, 0, name='infected')
    nx.set_node_attributes(G, 0, name='recovered')
    for node in infected_nodes:
        G.nodes[node]['infected'] = 1

    # G.remove_nodes_from(list(nx.isolates(G)))

    infected = nx.get_node_attributes(G, 'infected')
    colors = []
    for node in G.nodes:
        if infected[node] == 1:
            colors.append('red')
        else:
            colors.append('yellow')

    full_path = path + '/' + filename
    nx.draw_networkx(G, node_size=5, width=0.1, node_color=colors, with_labels=False)
    plt.show()
    if save:
        nx.write_gml(G, full_path)


if __name__ == '__main__':
    main()
