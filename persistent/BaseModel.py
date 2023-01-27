import os

import peewee as pw
from dotenv import load_dotenv

load_dotenv()

db = None
if db is None:
    db = pw.SqliteDatabase(f"db/{os.environ.get('DB_NAME')}")


class BaseModel(pw.Model):

    @staticmethod
    def get_db():
        return db

    @staticmethod
    def create_tables():
        db.create_tables(BaseModel.__subclasses__())

    class Meta:
        database = db
