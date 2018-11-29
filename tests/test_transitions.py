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
