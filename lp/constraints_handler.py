from lp.constraints.cumulative_constraints import add_cumulative_constraints
from lp.constraints.flipper_constraints import add_flipper_constraints
from lp.constraints.triangle_constraints import add_triangle_constraints
from lp.constraints.twin_nodes_constraints import set_twin_nodes_constraints


def create_constraints(solver, variables, g, b, s, l):
    add_flipper_constraints(solver, variables, l)
    add_triangle_constraints(solver, variables, l)
    twins_counter = set_twin_nodes_constraints(solver, variables, g, b, s, l)
    add_cumulative_constraints(solver, variables, b, s, l)
    return solver.NumConstraints(), twins_counter
