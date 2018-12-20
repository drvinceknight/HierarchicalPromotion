import itertools


def get_level_states(capacity):
    for type_0 in range(capacity + 1):
        yield type_0, capacity - type_0

    for type_0 in range(capacity):
        yield type_0, capacity - 1 - type_0


def get_states(capacities):
    all_states = itertools.product(
        *[get_level_states(capacity) for capacity in capacities]
    )
    invalid_state = lambda state: sum(state[-1]) != capacities[-1]
    return itertools.filterfalse(invalid_state, all_states)


def enumerate_states(capacities):
    cardinality = capacities[-1] + 1
    for capacity in capacities[:-1]:
        cardinality *= 2 * capacity + 1
    return cardinality
