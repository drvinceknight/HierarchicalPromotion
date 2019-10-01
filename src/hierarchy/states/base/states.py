import itertools

import numpy as np


def get_level_states(capacity):
    for type_0 in range(capacity + 1):
        yield type_0, capacity - type_0

    for type_0 in range(capacity):
        yield type_0, capacity - 1 - type_0


def get_states(capacities):
    assert capacities[-1] == 1
    all_states = itertools.product(
        *[get_level_states(capacity) for capacity in capacities]
    )
    invalid_state = lambda state: not np.array_equal(state[-1], [1, 0])
    return itertools.filterfalse(invalid_state, all_states)


def enumerate_states(capacities):
    assert capacities[-1] == 1
    cardinality = 1
    for capacity in capacities[:-1]:
        cardinality *= 2 * capacity + 1
    return cardinality
