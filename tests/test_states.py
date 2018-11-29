import hierarchy as hrcy
import types

def test_get_states():
    assert type(hrcy.states.get_states()) is types.GeneratorType

def test_get_level_states():
    capacity = 3
    states_generators = hrcy.states.get_level_states(capacity=capacity)
    assert type(states_generators) is types.GeneratorType

    states = list(states_generators)
    assert states == [ (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2),
                       (2, 0), (2, 1), (3, 0)]