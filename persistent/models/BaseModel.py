import os

import peewee as pw
from dotenv import load_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase

load_dotenv()

db = None
if db is None:
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db = PostgresqlExtDatabase(db_name, host='localhost', port=5432, user=db_user, password=db_password)


class BaseModel(pw.Model):

    @staticmethod
    def get_db():
        return db

    @staticmethod
    def create_tables():
        db.create_tables(BaseModel.__subclasses__())

    class Meta:
        database = db
