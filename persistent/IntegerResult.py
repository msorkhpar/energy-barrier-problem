import datetime
import peewee as pw
from playhouse.sqlite_ext import JSONField
from persistent.BaseModel import BaseModel
from persistent.BipartiteGraph import BipartiteGraph


class IntegerResult(BaseModel):
    result_id = pw.AutoField()
    bipartite_graph = pw.ForeignKeyField(BipartiteGraph, backref='integer_result')
    k = pw.IntegerField(default=-1)
    values = JSONField()
    sequence = JSONField()
    created_date = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'integer_result'
