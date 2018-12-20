import numpy as np

import hierarchy as hrcy


def get_stationary_distribution(capacities, r, lmbda, mu):
    matrix = hrcy.transitions.get_transition_matrix(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )

    dimension = matrix.shape[0]
    M = np.vstack((matrix.transpose(), np.ones(dimension)))
    b = np.vstack((np.zeros((dimension, 1)), [1]))

    return np.linalg.lstsq(M, b)[0].transpose()[0]
