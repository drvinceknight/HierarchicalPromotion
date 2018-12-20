import hierarchy as hrcy

capacities = [5, 3, 1]
state = [[3, 2], [1, 2], [1, 0]]


def test_state_to_tikz_output():
    tikz_code = hrcy.state_to_tikz(capacities=capacities, state=state)
    expected_tikz_code = """\\node[circle, draw=black, dashed, fill=blue] (0) at (0, 0) {};\\node[circle, draw=black, dashed, fill=blue] (1) at (1, 0) {};\\node[circle, draw=black, dashed, fill=blue] (2) at (2, 0) {};\\node[circle, draw=black, dotted, fill=red] (3) at (3, 0) {};\\node[circle, draw=black, dotted, fill=red] (4) at (4, 0) {};\\node[circle, draw=black, dashed, fill=blue] (5) at (0, 1) {};\\node[circle, draw=black, dotted, fill=red] (6) at (1, 1) {};\\node[circle, draw=black, dotted, fill=red] (7) at (2, 1) {};\\node[circle, draw=black, dashed, fill=blue] (8) at (0, 2) {};\\node[circle, draw=black, fill=black]  (9) at (1, 2) {};"""
    assert tikz_code == expected_tikz_code


def test_draw_included_edges():
    tikz_code = hrcy.state_to_tikz(
        capacities=capacities, state=state, include_edges=True
    )
    assert r"\draw" in tikz_code


def test_draw_include_boiler_plate():
    tikz_code = hrcy.state_to_tikz(
        capacities=capacities, state=state, include_boiler_plate=True
    )
    assert r"\begin{document}" in tikz_code
    assert r"\end{document}" in tikz_code
