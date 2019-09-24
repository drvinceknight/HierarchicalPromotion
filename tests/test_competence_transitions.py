import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_next_state_retirement():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]
    last_retirement = 0
    lmbda = [2, 3]
    Gamma = 5

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

    state_out, out_last_retirement = hrcy.transitions.get_competence_next_state(
        state_in=state_in,
        capacities=capacities,
        last_retirement=last_retirement,
        lmbda=lmbda,
        competence_distribution=distribution,
        retirement_rate=retirement_rate,
        Gamma=Gamma,
    )

    assert out_last_retirement != last_retirement
    for level in [0, -1]:
        assert [
            individual.individual_type for individual in state_out[level]
        ] == [individual.individual_type for individual in state_in[level]]
    assert state_out[1][0] == None
    assert state_out[1][1].individual_type == state_in[1][1].individual_type


def test_get_next_state_hire():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]
    last_retirement = 0
    lmbda = [2, 3]
    Gamma = (5,)
    seed = 5

    np.random.seed(seed)
    state_in = [
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
    state_out, out_last_retirement = hrcy.transitions.get_competence_next_state(
        state_in=state_in,
        capacities=capacities,
        last_retirement=last_retirement,
        lmbda=lmbda,
        competence_distribution=distribution,
        retirement_rate=retirement_rate,
        Gamma=Gamma,
        seed=seed,
    )
    expected_type_of_individual = 0

    assert out_last_retirement == last_retirement
    for level in [1, 2]:
        assert [
            individual.individual_type for individual in state_out[level]
        ] == [individual.individual_type for individual in state_in[level]]
    assert state_out[0][0].individual_type == expected_type_of_individual
    assert state_out[0][0].retirement_date > last_retirement


def test_get_next_state_promote():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]
    last_retirement = 0
    lmbda = [2, 3]
    Gamma = 10
    seed = 10

    np.random.seed(seed)
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
            for individual_type in [0]
        ]
        + [None],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]
    state_out, out_last_retirement = hrcy.transitions.get_competence_next_state(
        state_in=state_in,
        capacities=capacities,
        last_retirement=last_retirement,
        lmbda=lmbda,
        competence_distribution=distribution,
        retirement_rate=retirement_rate,
        Gamma=Gamma,
        seed=seed,
    )
    expected_type_of_promoted_individual = 0

    assert out_last_retirement == last_retirement
    assert [individual.individual_type for individual in state_out[0][:-1]] == [
        1,
        1,
    ]
    assert (
        state_out[1][1].individual_type == expected_type_of_promoted_individual
    )


def test_make_retirement():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
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

    state_out, last_retirement = hrcy.transitions.make_retirement(state_in)

    assert np.isclose(last_retirement, 0.5096501012053217)
    assert state_out[0][0] == None


def test_make_hire():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    lmbda = [2, 3]
    last_retirement = 2

    np.random.seed(1)
    state_in = [
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
            for individual_type in [1, 1]
        ],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]
    state_out = hrcy.transitions.make_hire(
        state_in,
        lmbda=lmbda,
        competence_distribution=distribution,
        retirement_rate=retirement_rate,
        last_retirement=last_retirement,
    )
    expected_individual_type = 1

    assert state_out[0][0].individual_type == expected_individual_type
    assert state_out[0][0].retirement_date > last_retirement


def test_make_promotion():
    distribution = scipy.stats.uniform(0, 1)
    retirement_rate = 0.4
    capacities = [3, 2, 1]
    Gamma = 20

    np.random.seed(10)
    state_in = [
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1, 0, 0]
        ],
        [
            hrcy.states.Individual(
                individual_type=individual_type,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
            for individual_type in [1]
        ]
        + [None],
        [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=distribution,
                retirement_rate=retirement_rate,
            )
        ],
    ]
    state_out = hrcy.transitions.make_promotion(state_in, capacities, Gamma)

    expected_promoted_index = 0
    expected_promoted_type = 1

    assert state_out[1][1].individual_type == expected_promoted_type
    assert state_out[0][expected_promoted_index] == None
