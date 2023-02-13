class Solution:
    def __init__(self, number_of_covered_neighborhood, number_of_twins,
                 variables_no, constraints_no):
        self.number_of_covered_neighborhood: int = number_of_covered_neighborhood
        self.number_of_twins: int = number_of_twins
        self.variables_no: int = variables_no
        self.constraints_no: int = constraints_no
        self.k: float = -1.0
        self.values: dict = {}
        self.sequence: list = []
        self.solution_time: float = -1.0

    def set_k(self, k):
        self.k = k

    def set_values(self, values):
        self.values = values

    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_solution_time(self, solution_time):
        self.solution_time = solution_time
