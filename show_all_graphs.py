import os
import sys
import networkx as nx
import matplotlib.pylab as plt

def main():
    path = 'examples/generated_graphs'

    if len(sys.argv) >= 2:
        path = sys.argv[1]

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

            nx.draw_networkx(G, node_size=6, width=0.1, node_color=colors, with_labels=False)
            plt.show()


if __name__ == '__main__':
    main()