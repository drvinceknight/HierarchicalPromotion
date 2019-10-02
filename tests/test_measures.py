import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_ratio_of_types_zero_in_state():
    state = [[3, 0], [1, 0], [1, 0]]
    ratio = hrcy.measures.get_ratio_of_types_zero_in_state(state)
    assert ratio == 1

    state = [[3, 1], [1, 0], [1, 0]]
    ratio = hrcy.measures.get_ratio_of_types_zero_in_state(state)
    assert ratio == 0.8

    state = [[4, 1], [2, 1], [1, 0]]
    ratio = hrcy.measures.get_ratio_of_types_zero_in_state(state)
    assert ratio == 0.75


def test_get_state_competence():
    capacities = [2, 1]
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4

    np.random.seed(0)
    potential_states = list(
        hrcy.states.get_competence_states(
            capacities, distribution, retirement_rate
        )
    )

    list_of_expected_competence = [
        1.9297336309488191,
        1.6393987615514476,
        2.5335445495335445,
        1.3462013120437828,
        0.8491928091477374,
    ]

    for state, expected_competence in zip(
        potential_states, list_of_expected_competence
    ):
        assert hrcy.measures.get_state_competence(state) == expected_competence
