import itertools
import types

import numpy as np
import scipy.stats

import hierarchy as hrcy


def test_get_states():
   capacities = [2, 1]
   distribution = scipy.stats.uniform(0, 1)
   states_generator = hrcy.states.get_competence_states(capacities, distribution)
   assert type(states_generator) is itertools.filterfalse

   expected_types_of_states = list(
       itertools.product([(0, 2), (1, 1), (2, 0), (0, 1), (1, 0)], [(1, 0)])
   )
   states = list(states_generator)
   types_in_states = [tuple([
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
    ]) for level in states]
   assert types_in_states == expected_types_of_states


def test_get_level_states():
    capacity = 3
    distribution = scipy.stats.uniform(0, 1)
    states_generators = hrcy.states.get_competence_level_states(
        capacity=capacity, competence_distribution=distribution
    )
    assert type(states_generators) is types.GeneratorType

    states = list(states_generators)
    types_in_states = [
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
        for state in states
    ]
    assert types_in_states == [
        (0, 3),
        (1, 2),
        (2, 1),
        (3, 0),
        (0, 2),
        (1, 1),
        (2, 0),
    ]
