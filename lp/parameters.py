import utility.utils
import utility.json_utils
import networkx as nx
from ortools.linear_solver import pywraplp


class Parameters:
    def __init__(self, g: nx.Graph, b_len, s_len, with_fractional_results, prices: dict[int:int] = None):
        self.g: nx.Graph = g
        self.b_len: int = b_len
        self.s_len: int = s_len
        self.l_len: int = b_len + s_len
        self.with_fractional_results: bool = with_fractional_results
        self.prices: dict[int, int] = prices
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.b: list = list(range(b_len))
        self.s: list = list(range(b_len, b_len + s_len))
        self.l: list = self.b + self.s
        self.variables: list = list()

    def var(self, i, j):
        return self.variables[self.to_index(i, j)]

    def to_index(self, i, j):
        return utility.utils.to_index(self.l_len, i, j)

    def from_index(self, index):
        return utility.utils.from_index(self.l_len, index)

    def set_variables(self, variables):
        self.variables = variables

    def add_constraint(self, constraint_rule):
        self.solver.Add(constraint_rule)
