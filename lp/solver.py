from ortools.linear_solver import pywraplp

from lp.constraints_handler import create_constraints
from utility.utils import from_index
from lp.variables_handler import create_variables
import numpy as np


def __create_nodes_sequence(values, l_len):
    sequence = {i: 0 for i in range(l_len)}
    for variable, value in values.items():
        if value == 1:
            i_index, j_index = from_index(variable)
            sequence[i_index] += 1
    return list(dict(sorted(sequence.items(), key=lambda x: x[1], reverse=True)).keys())


def __create_solver():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    return solver


def solve(g, b_len, s_len, with_fractional_results):
    b = list(range(b_len))
    s = list(range(b_len, b_len + s_len))
    l = b + s

    solver = __create_solver()

    if not solver:
        print("Could not create solver")
        return

    # Preparation
    variables, variables_no, covered_neighborhood = create_variables(solver, g, b, s, l, with_fractional_results)
    constraints_no, twins_counter = create_constraints(solver, variables, g, b, s, l)

    # Objective function
    solver.Minimize(variables[solver.NumVariables() - 1])
    status = solver.Solve()

    solution = {
        "k": -1, "values": [], "number_of_covered_neighborhood": covered_neighborhood,
        "number_of_twins": twins_counter, "variables_no": variables_no, "constraints_no": constraints_no,
        "sequence": None
    }
    values = {}
    if status == pywraplp.Solver.OPTIMAL:
        k = variables[solver.NumVariables() - 1].solution_value()
        k = np.round(k, 4)
        for var_index in range(solver.NumVariables() - 1):
            values[var_index] = variables[var_index].solution_value()
        solver.Clear()
        sequence = None
        if not with_fractional_results:
            sequence = __create_nodes_sequence(values, b_len + s_len)
        solution.update({"k": k, "values": values, "sequence": sequence})
        return solution
    else:
        print('The given problem does not have an optimal solution.')
        solver.Clear()
        return solution
