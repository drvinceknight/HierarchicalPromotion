import itertools
import random

head = r"""
\documentclass{standalone}

\usepackage{tikz}
\usepackage{standalone}
\usetikzlibrary{calc}

\begin{document}

\begin{tikzpicture}"""

tail = r"""
\end{tikzpicture}
\end{document}"""

def color_distribution(capacities, of_type_one):
    distributions = []
    for capacity, number_of_type_one in zip(capacities, of_type_one):
        distribution = ['blue' for _ in range(number_of_type_one)]
        distribution += ['red' for _ in range(capacity - number_of_type_one)]

        random.shuffle(distribution)
        distributions.append(distribution)
    return distributions

def draw_system_using_tikz(capacities, of_type_one, filename):
    write_nodes = ""
    node_number = 0
    nodes_sets = []
    colors = color_distribution(capacities=capacities, of_type_one=of_type_one)

    for layer, capacity in enumerate(capacities):
        nodes_subset = []
        for indv, color in zip(range(capacity), colors[layer]):
            write_nodes += r"\node[circle, draw=black, fill=%s]  (%s) at (%s, %s) {};" 
                                      % (color, node_number, indv, layer) + "\n"
            nodes_subset.append(node_number)
            node_number += 1
        nodes_sets.append(nodes_subset)

    write_edges = ""
    for i, _ in enumerate(nodes_sets[:-1]):
        for pair in itertools.product(nodes_sets[i], nodes_sets[i + 1]):
            write_edges += r"\draw (%s) -- (%s);" % (pair) + "\n"

    file = open(filename,"w")
    for lines in [head, write_nodes, write_edges, tail]:
        file.write(lines)
    file.close()