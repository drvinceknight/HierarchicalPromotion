import itertools
import types

import hierarchy as hrcy


def test_get_states():
    capacities = [2, 1]
    states_generator = hrcy.states.get_states(capacities)
    assert type(states_generator) is itertools.filterfalse

    expected_states = list(
        itertools.product(
            [(0, 2), (1, 1), (2, 0), (0, 1), (1, 0)], [(0, 1), (1, 0)]
        )
    )
    assert list(states_generator) == expected_states


def test_get_level_states():
    capacity = 3
    states_generators = hrcy.states.get_level_states(capacity=capacity)
    assert type(states_generators) is types.GeneratorType

    states = list(states_generators)
    assert states == [(0, 3), (1, 2), (2, 1), (3, 0), (0, 2), (1, 1), (2, 0)]


def test_enumerate_states():
    capacities = [2, 1]
    states = list(hrcy.states.get_states(capacities))
    assert len(states) == hrcy.states.enumerate_states(capacities)

    capacities = [4, 3, 1]
    states = list(hrcy.states.get_states(capacities))
    assert len(states) == hrcy.states.enumerate_states(capacities)

    capacities = [5, 4, 2, 1]
    states = list(hrcy.states.get_states(capacities))
    assert len(states) == hrcy.states.enumerate_states(capacities)
