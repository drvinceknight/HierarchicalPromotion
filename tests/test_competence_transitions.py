import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_next_state_retirement():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]

    np.random.seed(0)
    state_in = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]

    state_out, _ = hrcy.transitions.get_competence_next_state(
        state_in, capacities
    )

    expected_state_out = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 1, 0]
        ],
        [
            None,
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            ),
        ],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]
    for level in [0, -1]:
        assert [
            individual.individual_type for individual in state_out[level]
        ] == [
            individual.individual_type
            for individual in expected_state_out[level]
        ]
    assert state_out[1][0] == expected_state_out[1][0]
    assert (
        state_out[1][1].individual_type
        == expected_state_out[1][1].individual_type
    )


def test_provoce_retirement():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]
    np.random.seed(1)
    state_in = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]

    expected_state_out = [
        [None]
        + [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]

    state_out, last_retirement = hrcy.transitions.get_competence_next_state(
        state_in, capacities
    )

    assert np.isclose(last_retirement, 0.5096501012053217)
    assert state_out[0][0] == expected_state_out[0][0]
