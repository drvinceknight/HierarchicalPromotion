import itertools
import types
import scipy.stats
import numpy as np

import hierarchy as hrcy


def test_individual_init():
    distribution = scipy.stats.uniform(0, 1)
    np.random.seed(0)
    individual = hrcy.states.Individual(
        individual_type=0,
        competence_distribution=distribution,
        retirement_rate=0.5,
        last_retirement_date=0,
    )
    assert individual.individual_type == 0
    assert np.isclose(individual.competence, 0.5488135039273248)
    assert np.isclose(individual.retirement_date, 0.6279653814829189)

    np.random.seed(1)
    individual = hrcy.states.Individual(
        individual_type=0,
        competence_distribution=distribution,
        retirement_rate=0.5,
        last_retirement_date=0,
    )
    assert individual.individual_type == 0
    assert np.isclose(individual.competence, 0.417022004702574)
    assert np.isclose(individual.retirement_date, 0.6370626265066521)

    np.random.seed(1)
    individual = hrcy.states.Individual(
        individual_type=1,
        competence_distribution=distribution,
        retirement_rate=0.5,
        last_retirement_date=0,
    )
    assert individual.individual_type == 1
    assert np.isclose(individual.competence, 0.417022004702574)
    assert np.isclose(individual.retirement_date, 0.6370626265066521)
