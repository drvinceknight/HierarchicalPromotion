import hierarchy as hrcy

capacities = [5, 3, 2]
state = [[3, 2], [1, 2], [1, 0]]


def test_state_to_tikz_is_of_type():
    tikz_code = hrcy.state_to_tikz(capacities=capacities, state=state)
    assert type(tikz_code) is str


def test_state_to_tikz():
    tikz_code = hrcy.state_to_tikz(capacities=capacities, state=state)
    assert r"\draw" not in tikz_code


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
