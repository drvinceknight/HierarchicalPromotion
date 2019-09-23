import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_potential_states_hire():
    capacities = [3, 2, 1]
    distribution = scipy.stats.uniform(0, 1)

    state_in = [
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            )
            for _ in range(2)
        ],
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            )
            for _ in range(2)
        ],
        [
            hrcy.states.Individual(
                individual_type=0, competence_distribution=distribution
            )
        ],
    ]

    potential_states = hrcy.transitions.get_competence_potential_states(
        state_in=state_in, capacities=capacities
    )
    states = list(potential_states)
    potential_types_in_states = [
        tuple(
            [
                (
                    np.sum(
                        individual.individual_type == 0
                        for individual in state
                        if individual is not None
                    ),
                    np.sum(
                        individual.individual_type == 1
                        for individual in state
                        if individual is not None
                    ),
                )
                for state in level
            ]
        )
        for level in states
    ]

    expected_states = ([[3, 1], [2, 0], [1, 0]], [[2, 2], [2, 0], [1, 0]])
    assert all(
        np.array_equal(potential, expected)
        for potential, expected in zip(
            potential_types_in_states, expected_states
        )
    )
