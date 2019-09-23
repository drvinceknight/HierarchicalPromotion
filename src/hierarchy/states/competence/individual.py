import numpy as np


class Individual:
    """
    A class for an individual in a competence based model
    """

    def __init__(
        self,
        individual_type,
        competence_distribution,
        retirement_rate,
        last_retirement,
    ):
        self.individual_type = individual_type
        self.competence = competence_distribution.rvs()
        self.retirement_date = last_retirement + np.random.exponential(
            retirement_rate
        )

    def __str__(self):
        return f"{self.individual_type}, {self.competence}"
