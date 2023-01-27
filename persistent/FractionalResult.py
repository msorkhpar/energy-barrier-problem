import datetime
import peewee as pw
from playhouse.sqlite_ext import JSONField
from persistent.BipartiteGraph import BipartiteGraph
from persistent.BaseModel import BaseModel


class FractionalResult(BaseModel):
    result_id = pw.AutoField()
    bipartite_graph = pw.ForeignKeyField(BipartiteGraph, backref='fractional_result')
    k = pw.DoubleField(default=-1)
    values = JSONField()
    created_date = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'fractional_result'
