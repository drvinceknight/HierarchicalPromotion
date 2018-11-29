import itertools

def get_level_states(capacity):
    for type_0 in range(capacity + 1):
        for type_1 in range(capacity + 1 - type_0):
            yield type_0, type_1

def get_states(capacities):
    all_states = itertools.product(*[get_level_states(capacity) for capacity in capacities])
    invalid_state = lambda state: sum(state[-1]) == 0 
    return itertools.filterfalse(invalid_state, all_states)
