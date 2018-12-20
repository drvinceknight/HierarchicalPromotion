import numpy as np

import hierarchy as hrcy


def test_simulation_seed_0():
    capacities = [3, 1]
    initial_state = [[2, 1], [1, 0]]
    r = 1.1
    lmbda = [2, 3]
    mu = [[0.2, 0.1], [1.2, 1.1]]
    seed = 0
    max_transitions = 10

    output = list(
        hrcy.get_simulated_history(
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            max_transitions=max_transitions,
            initial_state=initial_state,
            seed=seed,
        )
    )
    history, dates = map(list, zip(*output))

    assert len(history) == max_transitions
    assert all(all(np.sum(state, axis=1) <= capacities) for state in history)
    assert all(
        all(np.sum(state, axis=1) + 1 >= capacities) for state in history
    )
    assert np.array_equal(history[-1], [[0, 2], [1, 0]])

    assert len(dates) == max_transitions
    assert np.min(np.diff(dates)) >= 0
    assert dates[0] == 0


def test_simulation_seed_1():
    capacities = [3, 1]
    initial_state = [[2, 1], [1, 0]]
    r = 1.1
    lmbda = [2, 3]
    mu = [[0.2, 0.1], [1.2, 1.1]]
    seed = 1
    max_transitions = 10

    output = list(
        hrcy.get_simulated_history(
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            max_transitions=max_transitions,
            initial_state=initial_state,
            seed=seed,
        )
    )
    history, dates = map(list, zip(*output))

    assert len(history) == max_transitions
    assert all(all(np.sum(state, axis=1) <= capacities) for state in history)
    assert all(
        all(np.sum(state, axis=1) + 1 >= capacities) for state in history
    )
    assert np.array_equal(history[-1], [[1, 1], [1, 0]])

    assert len(dates) == max_transitions
    assert np.min(np.diff(dates)) >= 0
    assert dates[0] == 0


def test_simulation_seed_0_no_initial_state():
    capacities = [3, 1]
    r = 1.1
    lmbda = [2, 3]
    mu = [[0.2, 0.1], [1.2, 1.1]]
    seed = 1
    max_transitions = 1

    output = list(
        hrcy.get_simulated_history(
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            max_transitions=max_transitions,
            seed=seed,
        )
    )
    history, dates = map(list, zip(*output))

    assert len(history) == max_transitions
    assert np.array_equal(history, [[[1, 2], [1, 0]]])

    assert len(dates) == max_transitions
    assert dates == [0]
