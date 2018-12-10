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

def states_to_tikz(capacities, states, include_edges=False, include_boiler_plate=False):
    write_nodes = ""
    node_number = 0
    nodes_sets = []
    for layer, state in enumerate(states):
        nodes_in_layer = 0
        nodes_subset = []
        for type_i in range(state[0]):
            write_nodes += r"\node[circle, draw=black, dashed, fill=blue]  (%s) at (%s, %s) {};" % (node_number, nodes_in_layer, layer) + "\n"
            nodes_subset.append(node_number)
            node_number += 1
            nodes_in_layer += 1
        
        for type_j in range(state[1]):
            write_nodes += r"\node[circle, draw=black, dotted, fill=red]  (%s) at (%s, %s) {};" % (node_number, nodes_in_layer, layer) + "\n"
            nodes_subset.append(node_number)
            node_number += 1
            nodes_in_layer += 1
            
        while nodes_in_layer  < capacities[layer]:
            write_nodes += r"\node[circle, draw=black]  (%s) at (%s, %s) {};" % (node_number, nodes_in_layer, layer) + "\n"
            nodes_subset.append(node_number)
            node_number += 1
            nodes_in_layer += 1
        nodes_sets.append(nodes_subset)

    write_edges = ""
    if include_edges:
        for i, _ in enumerate(nodes_sets[:-1]):
            for pair in itertools.product(nodes_sets[i], nodes_sets[i + 1]):
                write_edges += r"\draw (%s) -- (%s);" % (pair) + "\n"

    tikz_code = write_nodes + write_edges

    if include_boiler_plate:
        tikz_code = head + tikz_code + tail

    return tikz_code
