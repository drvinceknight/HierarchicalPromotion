class Individual:
    """
    A class for an individual in a competence based model
    """

    def __init__(self, individual_type, competence_distribution):
        self.individual_type = individual_type
        self.competence = competence_distribution.rvs()

    def __str__(self):
        return f"{self.individual_type}, {self.competence}"
