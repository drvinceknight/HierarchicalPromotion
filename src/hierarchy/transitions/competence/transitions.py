import copy
import itertools

import numpy as np

import hierarchy as hrcy


def get_competence_next_state(
    state_in,
    capacities,
    last_retirement,
    lmbda,
    competence_distribution,
    retirement_rate,
    Gamma,
    seed=0,
):
    size = len(capacities)
    occupied_spaces = [
        sum(individual is not None for individual in level)
        for level in state_in
    ]

    if occupied_spaces == capacities:
        state_out, last_retirement = provoke_retirement(state_in)

        return state_out, last_retirement

    if (occupied_spaces[1:] == capacities[1:]) and (
        occupied_spaces[0] == capacities[0] - 1
    ):
        np.random.seed(seed)
        state_out = provoke_hire(
            state_in,
            lmbda,
            competence_distribution,
            retirement_rate,
            last_retirement,
        )

        return state_out, last_retirement

    if (occupied_spaces[0] == capacities[0]) and (
        occupied_spaces[1:] != capacities[1:]
    ):
        state_out = provoke_promotion(state_in, capacities, Gamma)

        return state_out, last_retirement


def provoke_retirement(state_in):
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


def provoke_hire(
    state_in, lmbda, competence_distribution, retirement_rate, last_retirement
):
    """
    Simulates a hire.

    lmbda is the rate of hiring each type of individual.
    """
    state_out = copy.deepcopy(state_in)
    probability_of_zero_hire = lmbda[0] / sum(lmbda)
    individual_type = np.random.choice(
        [0, 1], p=[probability_of_zero_hire, 1 - probability_of_zero_hire]
    )

    hiring_space = [
        index
        for index, individual in enumerate(state_out[0])
        if individual == None
    ]
    state_out[0][hiring_space[0]] = hrcy.states.Individual(
        individual_type=individual_type,
        competence_distribution=competence_distribution,
        retirement_rate=retirement_rate,
        last_retirement=last_retirement,
    )

    return state_out


def provoke_promotion(state_in, capacities, Gamma):
    state_out = copy.deepcopy(state_in)

    free_space = [
        (i, j)
        for i, level in enumerate(state_out)
        for j, _ in enumerate(level)
        if state_out[i][j] is None
    ]
    level_of_promotion, space_of_promotion = free_space[0]

    rates_for_each_individual = []
    for potential_promoted_individual in state_out[level_of_promotion - 1]:
        competence = 0
        for individual in state_in[level_of_promotion]:
            if individual is not None:
                gamma = np.random.randint(1, Gamma)
                competence += (
                    max(
                        (
                            (
                                1
                                - abs(
                                    individual.individual_type
                                    - potential_promoted_individual.individual_type
                                )
                            )
                            * gamma
                        ),
                        1,
                    )
                    * potential_promoted_individual.competence
                )

        rates_for_each_individual.append(competence)

    probalities_of_promotion_for_each_individual = [
        rate / sum(rates_for_each_individual)
        for rate in rates_for_each_individual
    ]
    individual_to_promote_index = np.random.choice(
        range(capacities[level_of_promotion - 1]),
        p=probalities_of_promotion_for_each_individual,
    )
    state_out[level_of_promotion][space_of_promotion] = state_out[
        level_of_promotion - 1
    ][individual_to_promote_index]
    state_out[level_of_promotion - 1][individual_to_promote_index] = None

    return state_out
