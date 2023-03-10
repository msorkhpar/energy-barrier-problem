import datetime
import peewee as pw
from playhouse.sqlite_ext import JSONField
from persistent.models.BaseModel import BaseModel
from persistent.models.SampleGraph import SampleGraph


class BipartiteGraph(BaseModel):
    bigraph_id = pw.AutoField()
    meta_info = pw.TextField(null=True)
    integer_k = pw.IntegerField(null=True)
    fractional_k = pw.DoubleField(null=True)
    b = pw.IntegerField()
    s = pw.IntegerField()
    edges = JSONField()
    b_graph = pw.ForeignKeyField(SampleGraph, backref='b_graph', null=True)
    s_graph = pw.ForeignKeyField(SampleGraph, backref='s_graph', null=True)
    number_of_edges = pw.IntegerField()
    number_of_covered_neighborhood = pw.IntegerField(null=True)
    number_of_twins = pw.IntegerField(null=True)
    integer_solution_time = pw.DoubleField(null=True)
    fractional_solution_time = pw.DoubleField(null=True)
    lp_variables_no = pw.IntegerField(null=True)
    lp_constraints_no = pw.IntegerField(null=True)
    node_mapping = JSONField()
    prices = JSONField(null=True)
    creation_date = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'bipartite_graph'
