# pylint: skip-file
import os
import sys
import networkx as nx
import matplotlib.pylab as plt

def main():
    path = 'examples/generated_graphs'
    path_to_save = ''

    if len(sys.argv) >= 2:
        path = sys.argv[1]
    if len(sys.argv) >= 3:
        path_to_save = sys.argv[2]

    files = os.listdir(path)
    for file in files:
        full_path = path + '/' + file
        G = None
        extension = file.split('.')[1]
        if extension == 'gml':
            G = nx.read_gml(full_path)

        if G:
            infected = nx.get_node_attributes(G, 'infected')
            recovered = nx.get_node_attributes(G, 'recovered')
            colors = []
            for node in G.nodes:
                if infected[node] == 1:
                    colors.append('red')
                elif recovered[node] == 1:
                    colors.append('green')
                else:
                    colors.append('yellow')

            fig, ax = plt.subplots()

            nx.draw_networkx(G, ax=ax, node_size=6, width=0.1, node_color=colors, with_labels=False)
            ax.set_title(file)

            if path_to_save:
                plt.savefig(path_to_save + '/' + ".".join(file.split('.')[0:-1]))
            else:
                plt.show()


if __name__ == '__main__':
    main()