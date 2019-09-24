import numpy as np
import hierarchy as hrcy


def get_competence_simulated_history(
    capacities,
    lmbda,
    competence_distribution,
    retirement_rate,
    Gamma,
    max_transitions,
    initial_state=None,
    seed=None,
):
    assert capacities[-1] == 1
    if seed is not None:
        np.random.seed(seed)

    if initial_state is None:
        initial_state = []
        for capacity in capacities[:-1]:
            number_of_zeros = np.random.randint(0, capacity)
            level = [
                hrcy.states.Individual(
                    individual_type=0,
                    competence_distribution=competence_distribution,
                    retirement_rate=retirement_rate,
                )
                for _ in range(number_of_zeros)
            ] + [
                hrcy.states.Individual(
                    individual_type=0,
                    competence_distribution=competence_distribution,
                    retirement_rate=retirement_rate,
                )
                for _ in range(capacity - number_of_zeros)
            ]
            initial_state.append(level)
        initial_state.append(
            [
                hrcy.states.Individual(
                    individual_type=0,
                    competence_distribution=competence_distribution,
                    retirement_rate=retirement_rate,
                )
            ]
        )

    state, last_retirement = (
        np.array([np.array(level) for level in initial_state]),
        0,
    )

    for _ in range(max_transitions):
        yield state, last_retirement
        state_out, last_retirement = hrcy.transitions.get_competence_next_state(
            state_in=state,
            capacities=capacities,
            last_retirement=last_retirement,
            lmbda=lmbda,
            competence_distribution=competence_distribution,
            retirement_rate=retirement_rate,
            Gamma=Gamma,
        )
        state = np.array([np.array(level) for level in state_out])
