from __future__ import annotations

from ortools.linear_solver import pywraplp

from lp.constraints_handler import create_constraints
from lp.parameters import Parameters
from lp.solution import Solution
from lp.variables_handler import create_variables
import numpy as np


class Solver:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def to_index(self, i, j):
        return self.parameters.to_index(i, j)

    def from_index(self, index):
        return self.parameters.from_index(index)

    def __create_nodes_sequence(self, values):
        sequence = {i: 0 for i in range(self.parameters.l_len)}
        for variable, value in values.items():
            if value == 1:
                i_index, j_index = self.from_index(variable)
                sequence[i_index] += 1
        return list(dict(sorted(sequence.items(), key=lambda x: x[1], reverse=True)).keys())

    def solve(self) -> Solution | None:
        if not self.parameters.solver:
            print("Could not create solver")
            return None

        solver = self.parameters.solver
        # Preparation
        covered_neighborhood = create_variables(self.parameters)

        twins_counter = create_constraints(self.parameters)
        constraints_no = self.parameters.solver.NumConstraints()
        variables_no = self.parameters.solver.NumVariables()
        # Objective function
        solver.Minimize(self.parameters.variables[variables_no - 1])
        status = self.parameters.solver.Solve()

        solution = Solution(covered_neighborhood, twins_counter, variables_no, constraints_no)
        values = {}
        if status == pywraplp.Solver.OPTIMAL:
            k = self.parameters.variables[solver.NumVariables() - 1].solution_value()
            k = np.round(k, 4)
            for var_index in range(variables_no - 1):
                values[var_index] = self.parameters.variables[var_index].solution_value()
            solver.Clear()
            sequence = None
            if not self.parameters.with_fractional_results:
                sequence = self.__create_nodes_sequence(values)
            solution.set_k(k)
            solution.set_values(values)
            solution.set_sequence(sequence)
            return solution
        else:
            print('The given problem does not have an optimal solution.')
            solver.Clear()
            return solution
