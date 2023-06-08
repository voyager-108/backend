import os
from peewee import *

_PG_KEYS = ["PGHOST", "PGUSER", "PGPASSWORD", "PGDATABASE", "PGPORT"]

if not all([key in os.environ for key in _PG_KEYS]):
    raise Exception("Missing Postgres environment variables. Please set all of the following: " + ", ".join(_PG_KEYS))

db_ref = PostgresqlDatabase(**{
    "host": os.environ["PGHOST"],
    "user": os.environ["PGUSER"],
    "password": os.environ["PGPASSWORD"],
    "port": os.environ["PGPORT"],
    "database": os.environ["PGDATABASE"]
})  

db_ref.connect()

class BaseModel(Model):
    class Meta:
        database = db_ref
