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
        last_retirement_date=0,
    ):
        self.individual_type = individual_type
        self.competence = competence_distribution.rvs()
        self.time_until_retirement = np.random.exponential(retirement_rate)
        self.retirement_date = self.time_until_retirement + last_retirement_date

    def __str__(self):
        return f"{self.individual_type}, {self.competence}"
