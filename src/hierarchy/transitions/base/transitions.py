import itertools

import numpy as np

import hierarchy as hrcy


def get_rate(state_in, state_out, capacities, r, lmbda, mu):
    """
    Obtain the transition rate for `state_in` -> `state_out`.

    - capacities: the capacities
    - r: the homophily rate (?)
    - lmbda: the hiring rate (vector of size 2)
    - mu: the retirement rate (matrix of same size as state space)
    """
    assert capacities[-1] == 1
    state_in = np.array(state_in)
    state_out = np.array(state_out)
    delta = state_out - state_in

    delta_indices = np.argwhere(delta)

    if len(delta_indices) == 1:
        i, j = delta_indices[0]
        if delta[i, j] == -1 and np.array_equal(
            np.sum(state_in, axis=1), capacities
        ):
            return mu[i][j]

        if delta[0, j] == 1 and sum(state_in[0]) == capacities[0] - 1:
            return lmbda[j]

    if len(delta_indices) == 2:
        i, j = delta_indices[1]
        if (
            i > 0
            and sum(state_in[i]) < capacities[i]
            and delta[i, j] == 1
            and delta[i - 1, j] == -1
        ):
            return max(r * state_in[i + 1, j] + state_in[i + 1, (j + 1) % 2], 1)
    return 0


def get_transition_matrix(capacities, r, lmbda, mu, digits=7):
    """
    Obtain the transition matrix.

    - capacities: the capacities
    - r: the homophily rate (?)
    - lmbda: the hiring rate (vector of size 2)
    - mu: the retirement rate (matrix of same size as state space)
    """
    assert capacities[-1] == 1
    states = list(hrcy.states.get_states(capacities=capacities))
    size = len(states)
    matrix = np.zeros((size, size))
    for i, j in itertools.product(range(size), repeat=2):
        state_in, state_out = states[i], states[j]
        rate = get_rate(
            state_in=state_in,
            state_out=state_out,
            capacities=capacities,
            r=r,
            lmbda=lmbda,
            mu=mu,
        )

        if rate != 0:
            matrix[i, j] = rate
    for i in range(size):
        matrix[i, i] = -sum(matrix[i])
    return np.round(matrix, digits)


def get_potential_states(state_in, capacities):
    """
    Return tuple of all potential next states for a given `state_in`
    """
    state_in = np.array(state_in)
    number_of_levels = len(capacities)
    states = []

    if is_full(state_in=state_in, capacities=capacities):
        for level in range(number_of_levels - 1):  # No retirement at top level
            for column in (0, 1):
                if state_in[level, column] > 0:
                    adjustment = np.zeros((number_of_levels, 2))
                    adjustment[level, column] = -1
                    states.append(state_in + adjustment)
        return states

    for level in find_free_levels(state_in=state_in, capacities=capacities):
        for column in (0, 1):
            adjustment = np.zeros((number_of_levels, 2))
            if level == 0:
                adjustment[level, column] = 1
                states.append(state_in + adjustment)
            elif state_in[level - 1, column] > 0:
                adjustment[level, column] = 1
                adjustment[level - 1, column] = -1
                states.append(state_in + adjustment)
    return states


def is_full(state_in, capacities):
    """
    A boolean to check if a given state is full.
    """
    return np.array_equal(np.sum(state_in, axis=1), capacities)


def find_free_levels(state_in, capacities):
    """
    A generator of the levels that have capacity
    """
    for level, (row, capacity) in enumerate(zip(state_in, capacities)):
        if np.sum(row) < capacity:
            yield level
