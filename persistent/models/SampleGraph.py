import datetime
import peewee as pw
from playhouse.sqlite_ext import JSONField
from persistent.models.BaseModel import BaseModel


class SampleGraph(BaseModel):
    graph_id = pw.AutoField()
    creation_date = pw.DateTimeField(default=datetime.datetime.now)
    number_of_nodes = pw.IntegerField()
    number_of_edges = pw.IntegerField()
    edges = JSONField()

    class Meta:
        table_name = 'sample_graph'
