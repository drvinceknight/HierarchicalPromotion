import itertools
import types

import hierarchy as hrcy


def test_get_transition_rate():
    capacities = [3, 2]
    state_in = [[2, 1], [1, 0]]
    state_out = [[2, 0], [1, 1]]
    r = 1.1
    lmbda = [2, 3]
    mu = [[.2, .1], [1.2, 1.1]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 1

    state_out = [[1, 1], [2, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 1.1

    state_out = [[2, 0], [2, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0

    state_out = [[2, 0], [1, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0

    state_out = [[1, 2], [1, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0
