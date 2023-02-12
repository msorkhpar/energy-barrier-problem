from lp.constraints.cumulative_constraints import add_cumulative_constraints
from lp.constraints.flipper_constraints import add_flipper_constraints
from lp.constraints.triangle_constraints import add_triangle_constraints
from lp.constraints.twin_nodes_constraints import set_twin_nodes_constraints
from lp.constraints.degree_twos_constraints import add_degree_twos_constraints
from lp.parameters import Parameters


def create_constraints(parameters: Parameters):
    add_flipper_constraints(parameters)
    add_triangle_constraints(parameters)
    twins_counter = set_twin_nodes_constraints(parameters)
    add_cumulative_constraints(parameters)
    add_degree_twos_constraints(parameters)
    return twins_counter
