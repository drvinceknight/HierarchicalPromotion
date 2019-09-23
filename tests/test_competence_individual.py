import itertools
import types
import scipy.stats
import numpy as np

import hierarchy as hrcy


def test_individual_init():
    distribution = scipy.stats.uniform(0, 1)
    np.random.seed(0)
    individual = hrcy.competence.Individual(individual_type=0,
            competence_distribution=distribution)
    assert individual.individual_type == 0
    assert np.isclose(individual.competence, 2)

    np.random.seed(1)
    individual = hrcy.competence.Individual(individual_type=0,
            competence_distribution=distribution)
    assert individual.individual_type == 0
    assert np.isclose(individual.competence, .5)

    np.random.seed(1)
    individual = hrcy.competence.Individual(individual_type=1,
            competence_distribution=distribution)
    assert individual.individual_type == 1
    assert np.isclose(individual.competence, .5)
