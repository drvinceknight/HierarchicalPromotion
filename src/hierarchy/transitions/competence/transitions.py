import itertools

import numpy as np

import hierarchy as hrcy


def get_types_in_state_from_competence_state(state):
    """
    Returns a competence state as a base model state.
    """
    types_in_state = [
        (
            np.sum(
                individual.individual_type == 0
                for individual in level
                if individual is not None
            ),
            np.sum(
                individual.individual_type == 1
                for individual in level
                if individual is not None
            ),
        )
        for level in state
    ]
    return types_in_state
