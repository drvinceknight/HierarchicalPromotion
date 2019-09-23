import itertools

import numpy as np

import hierarchy as hrcy


def get_competence_level_states(capacity, competence_distribution):
    for type_0 in range(capacity + 1):
        level = [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=competence_distribution,
            )
            for _ in range(type_0)
        ]
        level += [
            hrcy.states.Individual(
                individual_type=1,
                competence_distribution=competence_distribution,
            )
            for _ in range(capacity - type_0)
        ]

        yield level

    for type_0 in range(capacity):
        level = [
            hrcy.states.Individual(
                individual_type=0,
                competence_distribution=competence_distribution,
            )
            for _ in range(type_0)
        ]
        level += [
            hrcy.states.Individual(
                individual_type=1,
                competence_distribution=competence_distribution,
            )
            for _ in range(capacity - type_0 - 1)
        ]
        level += [None]

        yield level


def get_competence_states(capacities, competence_distribution):
    assert capacities[-1] == 1
    all_states = itertools.product(
        *[
            get_competence_level_states(
                capacity, competence_distribution=competence_distribution
            )
            for capacity in capacities
        ]
    )
    invalid_state = (
        lambda state: state[-1][0] is None or state[-1][0].individual_type == 1
    )
    return itertools.filterfalse(invalid_state, all_states)
