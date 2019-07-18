"""Acts as a library of all available networks"""
import networkx as nx


# general metrics
def static_degree_centrality(network: nx.Graph):
    r"""Compute the degree centrality for nodes.

        The degree centrality for a node v is the fraction of nodes it
        is connected to.

    Args:
        network: A NetworkX graph

    Returns
        dict: Dictionary of nodes with degree centrality as the value."""
    return nx.degree_centrality(network)


def static_hits(network: nx.Graph):
    r""""Returns HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Args:
        network : A NetworkX graph

    Returns:
    tuple: (hubs,authorities) two-tuple of dictionaries
            Two dictionaries keyed by node containing the hub and authority
            values.

    Raises:
        PowerIterationFailedConvergence: If the algorithm fails to converge to the specified tolerance
            within the specified number of iterations of the power iteration
            method."""
    try:
        return nx.hits_scipy(network)
    except nx.PowerIterationFailedConvergence:
        return None


def static_diameter(network: nx.Graph):
    r"""Returns the diameter of the graph G.

    The diameter is the maximum eccentricity.

    Args:
        network : a NetworkX graph

    Returns:
        d : Diameter of graph"""
    try:
        return nx.algorithms.distance_measures.diameter(network)
    except nx.NetworkXError:
        return 0


def static_density(network: nx.Graph):
    r"""Calculates density, based on Wikipedia

    Args:
        network: A NetworkX graph

    Returns:
        float: density"""
    edges = len(network.edges)
    vertices = len(network.nodes)
    return edges / (vertices * (vertices - 1))


def static_modularity(network):
    r"""Find communities in graph using Clauset-Newman-Moore greedy modularity
    maximization. This method currently supports the Graph class and does not
    consider edge weights.

    Greedy modularity maximization begins with each node in its own community
    and joins the pair of communities that most increases modularity until no
    such pair exists.

    Args:
        network : NetworkX graph

    Yields:
        Yields sets of nodes, one for each community.

    Examples:
        >>> from networkx.algorithms.community import greedy_modularity_communities
        >>> G = nx.karate_club_graph()
        >>> c = list(greedy_modularity_communities(G))
        >>> sorted(c[0])
        [8, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]"""
    return nx.algorithms.community.modularity_max.greedy_modularity_communities(network)


def static_page_rank(network: nx.Graph):
    r"""Returns the PageRank of the nodes in the graph.

    PageRank computes a ranking of the nodes in the graph G based on
    the structure of the incoming links. It was originally designed as
    an algorithm to rank web pages.

    Args:
        network : A NetworkX graph. Undirected graphs will be converted to a directed
      graph with two directed edges for each undirected edge.

    Returns:
        dict: Dictionary of nodes with PageRank as value

    Examples:
        >>> G = nx.DiGraph(nx.path_graph(4))
        >>> pr = nx.pagerank(G, alpha=0.9)

    Raises:
        PowerIterationFailedConvergence: If the algorithm fails to converge to the specified tolerance
            within the specified number of iterations of the power iteration
            method."""
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(network)


def static_eigenvector_centrality(network: nx.Graph):
    r"""Compute the eigenvector centrality for the graph `G`.

    Eigenvector centrality computes the centrality for a node based on the
    centrality of its neighbors. The eigenvector centrality for node $i$ is
    the $i$-th element of the vector $x$ defined by the equation

    .. math::

        Ax = \lambda x

    where $A$ is the adjacency matrix of the graph `G` with eigenvalue
    $\lambda$. By virtue of the Perron–Frobenius theorem, there is a unique
    solution $x$, all of whose entries are positive, if $\lambda$ is the
    largest eigenvalue of the adjacency matrix $A$ ([2]_).

    Args:
        network : A NetworkX graph

    Returns:
        dict: Dictionary of nodes with eigenvector centrality as the value.

    Examples:
        >>> G = nx.path_graph(4)
        >>> centrality = nx.eigenvector_centrality(G)
        >>> sorted((v, '{:0.2f}'.format(c)) for v, c in centrality.items())
        [(0, '0.37'), (1, '0.60'), (2, '0.60'), (3, '0.37')]

    Raises:
        NetworkXPointlessConcept: If the graph `G` is the null graph.

        NetworkXError: If each value in `nstart` is zero.

        PowerIterationFailedConvergence: If the algorithm fails to converge to the specified tolerance
            within the specified number of iterations of the power iteration
            method.
"""
    return nx.algorithms.centrality.eigenvector_centrality(network, max_iter=1000)


def static_closeness_centrality(network: nx.Graph):
    r"""Compute closeness centrality for nodes.

    Closeness centrality [1]_ of a node `u` is the reciprocal of the
    average shortest path distance to `u` over all `n-1` reachable nodes.

    .. math::

        C(u) = \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)},

    where `d(v, u)` is the shortest-path distance between `v` and `u`,
    and `n` is the number of nodes that can reach `u`. Notice that the
    closeness distance function computes the incoming distance to `u`
    for directed graphs. To use outward distance, act on `G.reverse()`.

    Notice that higher values of closeness indicate higher centrality.

    Wasserman and Faust propose an improved formula for graphs with
    more than one connected component. The result is "a ratio of the
    fraction of actors in the group who are reachable, to the average
    distance" from the reachable actors [2]_. You might think this
    scale factor is inverted but it is not. As is, nodes from small
    components receive a smaller closeness value. Letting `N` denote
    the number of nodes in the graph,

    .. math::

        C_{WF}(u) = \frac{n-1}{N-1} \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)},

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with closeness centrality as the value."""
    return nx.algorithms.centrality.closeness_centrality(network)


def static_betweenness_centrality(network: nx.Graph):
    r"""Compute the shortest-path betweenness centrality for nodes.

    Betweenness centrality of a node $v$ is the sum of the
    fraction of all-pairs shortest paths that pass through $v$

    .. math::

       c_B(v) =\sum_{s,t \in V} \frac{\sigma(s, t|v)}{\sigma(s, t)}

    where $V$ is the set of nodes, $\sigma(s, t)$ is the number of
    shortest $(s, t)$-paths,  and $\sigma(s, t|v)$ is the number of
    those paths  passing through some  node $v$ other than $s, t$.
    If $s = t$, $\sigma(s, t) = 1$, and if $v \in {s, t}$,
    $\sigma(s, t|v) = 0$ [2]_.

    Args:
        network: A NetworkX graph.

    Returns:
    dict: Dictionary of nodes with betweenness centrality as the value."""
    return nx.algorithms.centrality.betweenness_centrality(network)


def static_average_path(network: nx.Graph):
    r"""Returns the average shortest path length.

    The average shortest path length is

    .. math::

       a =\sum_{s,t \in V} \frac{d(s, t)}{n(n-1)}

    where `V` is the set of nodes in `G`,
    `d(s, t)` is the shortest path from `s` to `t`,
    and `n` is the number of nodes in `G`.

    Args:
        network: NetworkX graph

    Raises:
        NetworkXPointlessConcept: If `G` is the null graph (that is, the graph on zero nodes).

        NetworkXError: If `G` is not connected (or not weakly connected, in the case
            of a directed graph).

        ValueError: If `method` is not among the supported options.

    Examples:
        >>> G = nx.path_graph(5)
        >>> nx.average_shortest_path_length(G)
        2.0

        For disconnected graphs, you can compute the average shortest path
        length for each component

        >>> G = nx.Graph([(1, 2), (3, 4)])
        >>> for C in nx.connected_component_subgraphs(G):
        ...     print(nx.average_shortest_path_length(C))
        1.0
        1.0"""
    return nx.algorithms.shortest_paths.generic.average_shortest_path_length(network)


# specific metrics
def static_maximum_flow(network: nx.Graph, source, target):
    r"""Find a maximum single-commodity flow.

    Args:
        network: Edges of the graph are expected to have an attribute called
            'capacity'. If this attribute is not present, the edge is
            considered to have infinite capacity.
        source: Source node for the flow.
        target: Sink node for the flow.

    Returns:
        integer, float: Value of the maximum flow, i.e., net outflow from the source.
        dict: A dictionary containing the value of the flow that went through
            each edge."""
    try:
        return nx.algorithms.flow.maximum_flow_value(network, source, target)
    except nx.NetworkXError:
        return 0.0
    except nx.NetworkXUnbounded:
        return 0.0


def static_current_flow_closeness(network: nx.Graph):
    r"""Compute current-flow closeness centrality for nodes.

    Current-flow closeness centrality is variant of closeness
    centrality based on effective resistance between nodes in
    a network. This metric is also known as information centrality.

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with current flow closeness centrality as the value.
"""
    return nx.algorithms.centrality.current_flow_closeness_centrality(network.to_undirected())


def static_current_flow_betweenness(network: nx.Graph):
    r"""Compute current-flow betweenness centrality for nodes.

    Current-flow betweenness centrality uses an electrical current
    model for information spreading in contrast to betweenness
    centrality which uses shortest paths.

    Current-flow betweenness centrality is also known as
    random-walk betweenness centrality [2]_.

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with betweenness centrality as the value."""
    return nx.algorithms.centrality.current_flow_betweenness_centrality(network.to_undirected())


def static_load_centrality(network: nx.Graph):
    r"""Compute load centrality for nodes.

    The load centrality of a node is the fraction of all shortest paths that pass through that node.

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with centrality as the value."""
    return nx.algorithms.centrality.load_centrality(network)


def subgraph(network: nx.Graph):
    r"""Returns subgraph centrality for each node in G.

    Subgraph centrality  of a node `n` is the sum of weighted closed
    walks of all lengths starting and ending at node `n`. The weights
    decrease with path length. Each closed walk is associated with a
    connected subgraph ([1]_).

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with subgraph centrality as the value.

    Raises:
        NetworkXError: If the graph is not undirected and simple."""
    return nx.algorithms.centrality.subgraph_centrality(network.to_undirected())


def harmonic_centrality(network: nx.Graph):
    r"""Compute harmonic centrality for nodes.

    Harmonic centrality [1]_ of a node `u` is the sum of the reciprocal
    of the shortest path distances from all other nodes to `u`

    .. math::

        C(u) = \sum_{v \neq u} \frac{1}{d(v, u)}

    where `d(v, u)` is the shortest-path distance between `v` and `u`.

    Notice that higher values indicate higher centrality.

    Args:
        network: A NetworkX graph

    Returns:
        dict: Dictionary of nodes with harmonic centrality as the value."""
    return nx.algorithms.centrality.harmonic_centrality(network)


def static_global_reaching(network: nx.Graph):
    r"""Returns the global reaching centrality of a directed graph.

    The *global reaching centrality* of a weighted directed graph is the
    average over all nodes of the difference between the local reaching
    centrality of the node and the greatest local reaching centrality of
    any node in the graph [1]_. For more information on the local
    reaching centrality, see :func:`local_reaching_centrality`.
    Informally, the local reaching centrality is the proportion of the
    graph that is reachable from the neighbors of the node.

    Args:
        network: A NetworkX DiGraph.

    Returns:
        float: The global reaching centrality of the graph.

    Examples:
        >>> import networkx as nx
        >>> G = nx.DiGraph()
        >>> G.add_edge(1, 2)
        >>> G.add_edge(1, 3)
        >>> nx.global_reaching_centrality(G)
        1.0
        >>> G.add_edge(3, 2)
        >>> nx.global_reaching_centrality(G)
        0.75"""
    return nx.algorithms.centrality.global_reaching_centrality(network)


def static_percolation(network: nx.Graph):
    r"""Compute the percolation centrality for nodes.

    Percolation centrality of a node $v$, at a given time, is defined
    as the proportion of ‘percolated paths’ that go through that node.

    This measure quantifies relative impact of nodes based on their
    topological connectivity, as well as their percolation states.

    Percolation states of nodes are used to depict network percolation
    scenarios (such as during infection transmission in a social network
    of individuals, spreading of computer viruses on computer networks, or
    transmission of disease over a network of towns) over time. In this
    measure usually the percolation state is expressed as a decimal
    between 0.0 and 1.0.

    When all nodes are in the same percolated state this measure is
    equivalent to betweenness centrality.

    Args:
        network: A NetworkX graph.

    Returns:
        dict: Dictionary of nodes with percolation centrality as the value."""
    try:
        return nx.algorithms.centrality.percolation_centrality(network)
    except KeyError:
        return {}


def static_second_order_centrality(network: nx.Graph):
    r"""Compute the second order centrality for nodes of G.

    The second order centrality of a given node is the standard deviation of
    the return times to that node of a perpetual random walk on G:

    Args:
        network: A NetworkX connected and undirected graph.

    Returns:
        dict: Dictionary keyed by node with second order centrality as the value.

    Examples:
        >>> G = nx.star_graph(10)
        >>> soc = nx.second_order_centrality(G)
        >>> print(sorted(soc.items(), key=lambda x:x[1])[0][0]) # pick first id
        0

    Raises:
        NetworkXException: If the graph G is empty, non connected or has negative weights."""
    return nx.algorithms.centrality.second_order_centrality(network.to_undirected())
