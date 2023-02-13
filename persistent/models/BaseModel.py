import os

import peewee as pw
from dotenv import load_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase

load_dotenv()

db = None
if db is None:
    db_host = os.environ.get('DB_HOST')
    db_port = int(os.environ.get('DB_PORT', 5432))
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    mode = os.environ.get('GRAPH_GENERATOR_TYPE')
    if db_host == "docker":
        if mode == "RANDOM_BIGRAPH":
            db_host = "random-db"
        elif mode == "INTERSECTION":
            db_host = "intersection-db"

    db = PostgresqlExtDatabase(db_name, host=db_host, port=db_port, user=db_user, password=db_password)


class BaseModel(pw.Model):

    @staticmethod
    def get_db():
        return db

    @staticmethod
    def create_tables():
        db.create_tables(BaseModel.__subclasses__())

    class Meta:
        database = db
