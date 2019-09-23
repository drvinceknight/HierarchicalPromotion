import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_types_in_state_from_competence_state():
    distribution = scipy.stats.uniform(0, 1)

    state = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
            )
            for individual_type in [0, 1]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
            )
            for individual_type in [1, 0]
        ],
    ]

    expected_types_in_state = [(1, 1), (1, 1)]

    assert (
        hrcy.transitions.get_types_in_state_from_competence_state(state)
        == expected_types_in_state
    )


def test_get_potential_states_hire():
    capacities = [3, 2, 1]
    distribution = scipy.stats.uniform(0, 1)

    state_in = [
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            )
            for _ in range(2)
        ]
        + [None],
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
        state_in=state_in,
        capacities=capacities,
        competence_distribution=distribution,
    )
    states = list(potential_states)
    potential_types_in_states = [
        tuple(hrcy.transitions.get_types_in_state_from_competence_state(level))
        for level in states
    ]
    expected_states = ([[1, 2], [0, 2], [1, 0]], [[0, 3], [0, 2], [1, 0]])

    assert len(expected_states) == len(set(potential_types_in_states))
    assert all(
        np.array_equal(potential, expected)
        for potential, expected in zip(
            potential_types_in_states, expected_states
        )
    )


def test_get_potential_states_promotion():
    capacities = [3, 2, 1]
    distribution = scipy.stats.uniform(0, 1)

    state_in = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
            )
            for individual_type in [0, 1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            ),
            None,
        ],
        [
            hrcy.states.Individual(
                individual_type=0, competence_distribution=distribution
            )
        ],
    ]
    potential_states = hrcy.transitions.get_competence_potential_states(
        state_in=state_in,
        capacities=capacities,
        competence_distribution=distribution,
    )
    states = list(potential_states)
    potential_types_in_states = [
        tuple(hrcy.transitions.get_types_in_state_from_competence_state(level))
        for level in states
    ]

    expected_states = ([[1, 1], [1, 1], [1, 0]], [[2, 0], [0, 2], [1, 0]])
    assert len(expected_states) == len(potential_types_in_states)
    assert all(
        np.array_equal(potential, expected)
        for potential, expected in zip(
            potential_types_in_states, expected_states
        )
    )


def test_get_potential_states_retirement():
    capacities = [3, 2, 1]
    distribution = scipy.stats.uniform(0, 1)

    state_in = [
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            )
            for _ in range(3)
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
            )
            for individual_type in [0, 1]
        ],
        [
            hrcy.states.Individual(
                individual_type=0, competence_distribution=distribution
            )
        ],
    ]

    potential_states = hrcy.transitions.get_competence_potential_states(
        state_in=state_in,
        capacities=capacities,
        competence_distribution=distribution,
    )
    states = list(potential_states)
    potential_types_in_states = [
        tuple(hrcy.transitions.get_types_in_state_from_competence_state(level))
        for level in states
    ]

    expected_states = (
        [[0, 2], [1, 1], [1, 0]],
        [[0, 3], [0, 1], [1, 0]],
        [[0, 3], [1, 0], [1, 0]],
    )
    assert len(expected_states) == len(potential_types_in_states)
    assert all(
        np.array_equal(potential, expected)
        for potential, expected in zip(
            potential_types_in_states, expected_states
        )
    )


def test_get_potential_states_promotion_all_capacities_one():
    capacities = [1, 1, 1]
    distribution = scipy.stats.uniform(0, 1)
    state_in = [
        [
            hrcy.states.Individual(
                individual_type=1, competence_distribution=distribution
            )
        ],
        [None],
        [
            hrcy.states.Individual(
                individual_type=0, competence_distribution=distribution
            )
        ],
    ]

    potential_state = hrcy.transitions.get_competence_potential_states(
        state_in=state_in,
        capacities=capacities,
        competence_distribution=distribution,
    )
    states = list(potential_state)
    potential_types_in_states = [
        hrcy.transitions.get_types_in_state_from_competence_state(level)
        for level in states
    ]

    expected_states = [([[0, 0], [0, 1], [1, 0]])]
    assert len(expected_states) == len(potential_types_in_states)
    assert all(
        np.array_equal(potential, expected)
        for potential, expected in zip(
            potential_types_in_states, expected_states
        )
    )
