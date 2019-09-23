class Individual:
    """
    A class for an individual in a competence based model
    """
    def __init__(self, individual_type, competence_distribution):
        self.individual_type = individual_type
        self.competence = competence_distribution.rvs()
