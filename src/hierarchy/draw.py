import itertools
import random


def state_to_tikz(
    capacities,
    state,
    include_edges=False,
    include_boiler_plate=False,
    colors=["blue", "red", "black"],
    styles=["dashed", "dotted"],
):
    assert capacities[-1] == 1
    write_nodes = ""
    node_id = 0
    nodes_sets = []
    for level, row in enumerate(state):
        number_of_nodes_in_level = 0
        nodes_in_level = []
        for individual_type, style, colour in zip((0, 1), styles, colors):
            for individual in range(int(row[individual_type])):
                write_nodes += fr"\node[circle, draw=black, {style}, fill={colour}] ({node_id}) at ({number_of_nodes_in_level}, {level}) {{}};"
                nodes_in_level.append(node_id)
                node_id += 1
                number_of_nodes_in_level += 1

        while number_of_nodes_in_level < capacities[level]:
            write_nodes += fr"\node[circle, draw=black, fill={colors[-1]}]  ({node_id}) at ({number_of_nodes_in_level}, {level}) {{}};"
            nodes_in_level.append(node_id)
            node_id += 1
            number_of_nodes_in_level += 1
        nodes_sets.append(nodes_in_level)

    write_edges = ""
    if include_edges:
        for i, _ in enumerate(nodes_sets[:-1]):
            for pair in itertools.product(nodes_sets[i], nodes_sets[i + 1]):
                write_edges += fr"\draw ({pair[0]}) -- ({pair[1]});"

    tikz_code = write_nodes + write_edges

    if include_boiler_plate:
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
        tikz_code = head + tikz_code + tail

    return tikz_code
