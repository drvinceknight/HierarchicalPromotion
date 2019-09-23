import copy
import itertools

import numpy as np

import hierarchy as hrcy


def get_competence_next_state(state_in, capacities):
    size = len(capacities)
    occupied_spaces = [
        sum(individual is not None for individual in level)
        for level in state_in
    ]

    if occupied_spaces == capacities:
        state_out, last_retirement = provoce_retirement(state_in)

        return state_out, last_retirement


def provoce_retirement(state_in):
    """
    Simulates a retirement. The individual with the maximum retirement date
    leaves.
    """
    state_out = copy.deepcopy(state_in)
    retirement_dates = [
        [individual.retirement_date for individual in level]
        for level in state_out[:-1]
    ]
    _, max_index = max(
        (rate, (i, j))
        for i, level in enumerate(retirement_dates)
        for j, rate in enumerate(level)
    )

    i, j = max_index
    last_retirement = state_out[i][j].retirement_date
    state_out[i][j] = None
    return state_out, last_retirement
