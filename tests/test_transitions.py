import itertools
import types

import numpy as np

import hierarchy as hrcy


def test_get_transition_rate():
    capacities = [3, 2]
    state_in = [[2, 1], [1, 0]]
    state_out = [[2, 0], [1, 1]]
    r = 1.1
    lmbda = [2, 3]
    mu = [[.2, .1], [1.2, 1.1]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 1

    state_out = [[1, 1], [2, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 1.1

    state_out = [[2, 0], [2, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0

    state_out = [[2, 0], [1, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0

    state_out = [[1, 2], [1, 0]]
    assert hrcy.transitions.get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
            ) == 0

def test_get_transition_matrix():
    capacities = [2, 1]
    r = 1.1
    lmbda = [2, 3]
    mu = [[.2, .1], [1.2, 1.1]]

    matrix = hrcy.transitions.get_transition_matrix(capacities=capacities, r=r, lmbda=lmbda, mu=mu)
    assert np.array_equal(matrix.shape, np.array([10, 10]))

    expected_matrix = np.array([[-.1,  0  ,  0  ,  0  ,  0  ,  0  ,  0.1, 0  ,  0  ,  0 ],
                                [0  ,  -.1,  0  ,  0  ,  0  ,  0  ,  0  , 0.1,  0  ,  0 ],
                                [0  ,  0  ,  -.3,  0  ,  0  ,  0  ,  0.2, 0  ,  0.1,  0 ],
                                [0  ,  0  ,  0  ,  -.3,  0  ,  0  ,  0  , 0.2,  0  ,  0.1],
                                [0  ,  0  ,  0  ,  0  ,  -.2,  0  ,  0  , 0  ,  0.2,  0 ],
                                [0  ,  0  ,  0  ,  0  ,  0  ,  -.2,  0  , 0  ,  0  ,  0.2],
                                [3  ,  0  ,  2  ,  0  ,  0  ,  0  ,  -5 , 0  ,  0  ,  0 ],
                                [0  ,  3  ,  0  ,  2  ,  0  ,  0  ,  0  , -5 ,  0  ,  0 ],
                                [0  ,  0  ,  3  ,  0  ,  2  ,  0  ,  0  , 0  ,  -5 ,  0 ],
                                [0  ,  0  ,  0  ,  3  ,  0  ,  2  ,  0  , 0  ,  0  ,  -5 ]])
    assert np.allclose(matrix, expected_matrix)

def test_get_transition_matrix_example_two():
    capacities = [4, 2, 1]
    r = 1.1
    lmbda = [2, 3]
    mu = [[.2, .1,], [1.2, 1.1], [1.5, 1.7]]

    matrix = hrcy.transitions.get_transition_matrix(capacities=capacities, r=r, lmbda=lmbda, mu=mu)
    assert np.array_equal(matrix.shape, np.array([90, 90]))
    assert np.allclose(np.sum(matrix, axis=1), 0)


def test_get_potential_states_hire():
    capacities = [4, 2, 1]
    state_in = [[2, 1], [2, 0], [1, 0]]
    potential_states = hrcy.transitions.get_potential_states(state_in=state_in, capacities=capacities)
    expected_states = ([[3, 1], [2, 0], [1, 0]], [[2, 2], [2, 0], [1, 0]])
    assert all(np.array_equal(potential, expected) for potential, expected in zip(potential_states, expected_states))

def test_get_potential_states_promotion():
    capacities = [4, 2, 1]
    state_in = [[2, 2], [1, 0], [1, 0]]
    potential_states = hrcy.transitions.get_potential_states(state_in=state_in, capacities=capacities)
    expected_states = ([[2, 2], [2, 0], [1, 0]], [[2, 2], [1, 1], [1, 0]])
    assert all(np.array_equal(potential, expected) for potential, expected in zip(potential_states, expected_states))

def test_get_potential_states_retirement():
    capacities = [4, 2, 1]
    state_in = [[2, 2], [1, 1], [1, 0]]
    potential_states = hrcy.transitions.get_potential_states(state_in=state_in, capacities=capacities)
    expected_states = ([[1, 2], [1, 1], [1, 0]], 
                       [[2, 1], [1, 1], [1, 0]], 
                       [[2, 2], [0, 1], [1, 0]], 
                       [[2, 2], [1, 0], [1, 0]], 
                       )
    assert len(expected_states) == len(potential_states)
    assert all(np.array_equal(potential, expected) for potential, expected in
        zip(potential_states, expected_states))

def test_is_full():
    capacities = [4, 2, 1]
    state_in = [[2, 2], [2, 0], [1, 0]]
    assert hrcy.transitions.is_full(state_in=state_in, capacities=capacities)

    state_in = [[2, 2], [1, 0], [1, 0]]
    assert not hrcy.transitions.is_full(state_in=state_in, capacities=capacities)

def test_find_free_levels():
    capacities = [4, 2, 1]
    state_in = [[2, 2], [2, 0], [1, 0]]
    assert list(hrcy.transitions.find_free_levels(state_in=state_in, capacities=capacities)) == []

    state_in = [[2, 2], [1, 0], [1, 0]]
    assert list(hrcy.transitions.find_free_levels(state_in=state_in, capacities=capacities)) == [1]
