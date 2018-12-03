import numpy as np

import hierarchy as hrcy


def get_stationary_distribution(capacities, r, lmbda, mu):
    matrix = hrcy.transitions.get_transition_matrix(
        capacities=capacities, r=r, lmbda=lmbda, mu=mu
    )

    vals, vects = np.linalg.eig(matrix.transpose())
    zero_eigenvector = vects.transpose()[np.argmin(np.abs(vals))]
    total = sum(zero_eigenvector)
    return zero_eigenvector / total
