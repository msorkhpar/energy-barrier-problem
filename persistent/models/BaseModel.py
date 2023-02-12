import os

import peewee as pw
from dotenv import load_dotenv

load_dotenv()

db = None
if db is None:
    if os.environ.get('GRAPH_GENERATOR_TYPE') == "RANDOM_BIGRAPH":
        db_name = os.environ.get('RANDOM_DB_NAME')
    elif os.environ.get('GRAPH_GENERATOR_TYPE') == "INTERSECTION":
        db_name = os.environ.get('INTERSECTION_DB_NAME')
    else:
        db_name = "Default.db"

    db = pw.SqliteDatabase(f"./db/{db_name}", check_same_thread=False)


class BaseModel(pw.Model):

    @staticmethod
    def get_db():
        return db

    @staticmethod
    def create_tables():
        db.create_tables(BaseModel.__subclasses__())

    class Meta:
        database = db
