import collections
import random

import numpy as np

import hierarchy as hrcy


def get_simulated_history(
    capacities, r, lmbda, mu, max_transitions, initial_state=None, seed=None
):
    assert capacities[-1] == 1
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    if initial_state is None:
        initial_state = []
        for capacity in capacities[:-1]:
            number = random.randint(0, capacity)
            level = [number, capacity - number]
            initial_state.append(level)
        initial_state.append([1, 0])
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


def get_simulated_stationary_vector(
    capacities,
    r,
    lmbda,
    mu,
    max_transitions=1000,
    number_of_repetitions=100,
    initial_state=None,
    seed=None,
):
    all_history = collections.Counter()

    states = list(hrcy.states.get_states(capacities=capacities))

    for seed in range(number_of_repetitions):
        output = list(
            hrcy.get_simulated_history(
                capacities=capacities,
                r=r,
                lmbda=lmbda,
                mu=mu,
                max_transitions=max_transitions,
                seed=seed,
            )
        )
        history, dates = map(list, zip(*output))
        for state, time in zip(history, np.diff(dates)):
            all_history[tuple(map(tuple, state.astype(int)))] += time

    total = np.sum([v for v in all_history.values()])
    simulated_stationary_vector = np.array(
        [all_history.get(state, 0) / (total) for state in states]
    )

    return simulated_stationary_vector
