import random

import numpy as np

import hierarchy as hrcy


def get_simulated_history(
    capacities, r, lmbda, mu, max_transitions, initial_state=None, seed=None
):

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    if initial_state is None:
        initial_state = []
        for capacity in capacities:
            number = random.randint(0, capacity)
            level = [number, capacity - number]
            initial_state.append(level)

    state, date = np.array(initial_state), 0

    for _ in range(max_transitions):
        yield state, date

        potential_states = np.array(
            hrcy.transitions.get_potential_states(
                state_in=state, capacities=capacities
            )
        )

        rates = np.array(
            [
                hrcy.transitions.get_rate(
                    state_in=state,
                    state_out=state_out,
                    capacities=capacities,
                    r=r,
                    lmbda=lmbda,
                    mu=mu,
                )
                for state_out in potential_states
            ]
        )

        non_zero_rate_indices = np.where(rates)
        rates = rates[non_zero_rate_indices]
        potential_states = potential_states[non_zero_rate_indices]

        samples = np.random.exponential(1 / np.array(rates))

        state = potential_states[np.argmin(samples)]
        date += np.min(samples)
