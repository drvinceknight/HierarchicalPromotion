import copy
import itertools

import numpy as np

import hierarchy as hrcy


def get_competence_potential_states(
    state_in, capacities, competence_distribution
):
    """
    Return tuple of all potential next states for a given `state_in` with
    competence.
    """
    types_in_state_in = get_types_in_state_from_competence_state(state_in)

    potential_types_in_states = hrcy.transitions.get_potential_states(
        types_in_state_in, capacities
    )

    potential_states = []
    for potential_types in potential_types_in_states:
        delta = potential_types - types_in_state_in
        delta_indices = np.argwhere(delta)

        if len(delta_indices) == 1:
            i, j = delta_indices[0]

            if delta[i, j] == 1:
                potential_state = copy.deepcopy(state_in)
                potential_state[i].append(
                    hrcy.states.Individual(
                        individual_type=j,
                        competence_distribution=competence_distribution,
                    )
                )
                potential_states.append(potential_state)
            if delta[i, j] == -1:
                indices = [
                    index
                    for index, individual in enumerate(state_in[i])
                    if individual.individual_type == j
                ]
                for index_to_retire in indices:
                    potential_state = copy.deepcopy(state_in)
                    potential_state[i][index_to_retire] = None
                potential_states.append(potential_state)
        if len(delta_indices) == 2:
            i, j = delta_indices[0]
            if delta[i, j] == -1:
                indices = [
                    index
                    for index, individual in enumerate(state_in[i])
                    if individual.individual_type == j
                ]
                for index_to_promote in indices:
                    potential_state = copy.deepcopy(state_in)
                    potential_state[i + 1].append(
                        potential_state[i][index_to_promote]
                    )
                    potential_state[i][index_to_promote] = None
                potential_states.append(potential_state)
    return potential_states
