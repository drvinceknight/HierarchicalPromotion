import itertools

def get_level_states(capacity):
    for type_0 in range(capacity + 1):
        for type_1 in range(capacity + 1 - type_0):
            yield type_0, type_1

def create_states(capacities):
    pass

