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
        potential = list(
            hrcy.states.get_competence_states(
                capacities, competence_distribution, retirement_rate
            )
        )
        index = np.random.choice(range(len(potential)))
        initial_state = potential[index]
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
