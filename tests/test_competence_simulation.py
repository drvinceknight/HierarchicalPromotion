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
