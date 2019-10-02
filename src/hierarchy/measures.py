def get_ratio_of_types_zero_in_state(state):
    types_zero, types_one = list(zip(*state[:-1]))
    return sum(types_zero) / (sum(types_zero) + sum(types_one))


def get_state_competence(state):
    competence_in_state = [
        [
            individual.competence
            for individual in level
            if individual is not None
        ]
        for level in state
    ]

    return sum(
        [
            competence
            for competence_in_level in competence_in_state
            for competence in competence_in_level
        ]
    )
