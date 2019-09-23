import numpy as np

import hierarchy as hrcy


def test_stationary():
    capacities = [2, 1]
    r = 1.1
    lmbda = [2, 3]
    mu = [[0.2, 0.1], [1.2, 1.1]]

    matrix = hrcy.transitions.get_transition_matrix(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )
    pi = hrcy.get_stationary_distribution(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )

    assert np.allclose(pi @ matrix, 0)
    assert len(pi) == matrix.shape[0]
    assert np.min(pi) >= 0
    assert np.isclose(np.sum(pi), 1)


def test_stationary_example_two():
    capacities = [4, 2, 1]
    r = 1.1
    lmbda = [2, 3]
    mu = [[0.2, 0.1], [1.2, 1.1], [1.5, 1.7]]

    matrix = hrcy.transitions.get_transition_matrix(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )
    pi = hrcy.get_stationary_distribution(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )

    assert np.allclose(pi @ matrix, 0)
    assert len(pi) == matrix.shape[0]
    assert np.min(pi) >= -10 ** -7
    assert np.isclose(np.sum(pi), 1)
