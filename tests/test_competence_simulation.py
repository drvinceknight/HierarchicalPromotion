import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_competence_simulated_history():
    capacities = [3, 1]
    lmbda = [2, 3]
    competence_distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    seed = 0
    Gamma = 5
    max_transitions = 10

    output = list(
        hrcy.simulation.get_competence_simulated_history(
            capacities,
            lmbda,
            competence_distribution,
            retirement_rate,
            Gamma,
            max_transitions,
            initial_state=None,
            seed=seed,
        )
    )

    history, retirement_dates = map(list, zip(*output))

    assert len(history) == max_transitions

    assert len(retirement_dates) == max_transitions
    assert all(
        [
            retirement_dates[i] <= retirement_dates[i + 1]
            for i, _ in enumerate(retirement_dates[:-1])
        ]
    )
    assert retirement_dates[0] == 0


def test_simulation_for_old_failure():
    competence_distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [6, 5, 5, 4, 2, 1]
    lmbda = [1, 1]
    Gamma = 5
    max_transitions = 5000
    seed = 0

    output = list(
        hrcy.simulation.get_competence_simulated_history(
            capacities=capacities,
            lmbda=lmbda,
            competence_distribution=competence_distribution,
            retirement_rate=retirement_rate,
            Gamma=Gamma,
            max_transitions=max_transitions,
            initial_state=None,
            seed=seed,
        )
    )
    history, retirement_dates = map(list, zip(*output))

    assert len(history) == max_transitions

    assert len(retirement_dates) == max_transitions
    assert all(
        [
            retirement_dates[i] <= retirement_dates[i + 1]
            for i, _ in enumerate(retirement_dates[:-1])
        ]
    )
    assert retirement_dates[0] == 0
