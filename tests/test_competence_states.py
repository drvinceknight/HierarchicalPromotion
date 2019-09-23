import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_types_in_state_from_competence_state():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4

    state = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [0, 1]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0]
        ],
    ]

    expected_types_in_state = [(1, 1), (1, 1)]

    assert (
        hrcy.states.get_types_in_state_from_competence_state(state)
        == expected_types_in_state
    )


def test_get_states():
    capacities = [2, 1]
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    states_generator = hrcy.states.get_competence_states(
        capacities, distribution, retirement_rate
    )
    assert type(states_generator) is itertools.filterfalse

    expected_types_of_states = list(
        itertools.product([(0, 2), (1, 1), (2, 0), (0, 1), (1, 0)], [(1, 0)])
    )
    states = list(states_generator)
    types_in_states = [
        tuple(hrcy.states.get_types_in_state_from_competence_state(level))
        for level in states
    ]
    assert types_in_states == expected_types_of_states


def test_get_level_states():
    capacity = 3
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    states_generators = hrcy.states.get_competence_level_states(
        capacity=capacity,
        competence_distribution=distribution,
        retirement_rate=retirement_rate,
    )
    assert type(states_generators) is types.GeneratorType

    states = list(states_generators)
    types_in_states = hrcy.states.get_types_in_state_from_competence_state(states)
    print(types_in_states)
    assert types_in_states == [
        (0, 3),
        (1, 2),
        (2, 1),
        (3, 0),
        (0, 2),
        (1, 1),
        (2, 0),
    ]
