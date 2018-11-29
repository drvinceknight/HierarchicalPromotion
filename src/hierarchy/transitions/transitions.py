import numpy as np

def get_rate(
        state_in,
        state_out,
        capacities,
        r,
        lmbda,
        mu,
        ):
    """
    Obtain the transition rate for `state_in` -> `state_out`.

    - capacities: the capacities
    - r: the homophily rate (?)
    - lmbda: the hiring rate (vector of size 2)
    - mu: the retirement rate (matrix of same size as state space)
    """
    state_in = np.array(state_in)
    state_out = np.array(state_out)
    delta = state_out - state_in

    delta_indices = np.argwhere(delta)

    if len(delta_indices) == 1:
        i, j = delta_indices[0]
        if (delta[i, j] == -1 
            and np.array_equal(np.sum(state_in, axis=1), capacities)):
            return mu[i][j]

        if delta[0, j] == 1 and sum(state_in[0]) == capacities[0] - 1:
            return lmbda[j]


    if len(delta_indices) == 2:
        i, j = delta_indices[1]
        if (i > 0 
            and sum(state_in[i]) < capacities[i] 
            and delta[i, j] == 1 
            and delta[i - 1, j] == -1):
            return r * state_in[i, j] + state_in[i, (j + 1) % 2]

    return 0
