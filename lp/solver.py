import os

from ortools.linear_solver import pywraplp

from lp.degree_one_constraints import add_degree_one_constraints
from lp.degree_twos_constraints import add_degree_twos_constraints
from lp.twin_nodes_constraints import set_twin_nodes_constraints
from lp.utils import from_index
from lp.variables_generator import create_variables
from lp.flipper_constraints import add_flipper_constraints
from lp.triangle_constraints import add_triangle_constraints
from lp.cumulative_constraints import add_cumulative_constraints
import numpy as np


def __create_nodes_sequence(values, l_len):
    sequence = {i: 0 for i in range(l_len)}
    for variable, value in values.items():
        if value == 1:
            i_index, j_index = from_index(variable)
            sequence[i_index] += 1
    return list(dict(sorted(sequence.items(), key=lambda x: x[1], reverse=True)).keys())


def solve(g, b_len, s_len, with_fractional_results, no_threads):
    b = list(range(b_len))
    s = list(range(b_len, b_len + s_len))
    l = b + s

    solver = pywraplp.Solver.CreateSolver('SCIP')
    solver.SetNumThreads(no_threads)

    if not solver:
        print("Could not create solver")
        return

    variables, number_of_covered_neighborhood = create_variables(solver, g, b, s, l, with_fractional_results)
    add_flipper_constraints(solver, variables, l)
    add_triangle_constraints(solver, variables, l)
    twins_counter = set_twin_nodes_constraints(solver, variables, g, b, s, l)
    add_cumulative_constraints(solver, variables, b, s, l)
    add_degree_one_constraints(solver, variables, g, b, l)
    add_degree_twos_constraints(solver, variables, g, s)

    variables_no = solver.NumVariables()
    constraints_no = solver.NumConstraints()
    solver.Minimize(variables[solver.NumVariables() - 1])
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        k = variables[solver.NumVariables() - 1].solution_value()
        k = np.round(k, 4)
        for var_index in range(solver.NumVariables() - 1):
            result[var_index] = variables[var_index].solution_value()
        solver.Clear()
        sequence = None
        if not with_fractional_results:
            sequence = __create_nodes_sequence(result, b_len + s_len)
        return {
            "k": k, "values": result, "number_of_covered_neighborhood": number_of_covered_neighborhood,
            "number_of_twins": twins_counter, "variables_no": variables_no, "constraints_no": constraints_no,
            "sequence": sequence
        }
    else:
        print('The problem does not have an optimal solution.')
        return {
            "k": -1, "values": [], "number_of_covered_neighborhood": number_of_covered_neighborhood,
            "number_of_twins": twins_counter, "variables_no": variables_no, "constraints_no": constraints_no,
            "sequence": None,
        }
