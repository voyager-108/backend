from database import BaseModel, CharField, AutoField, FloatField, ForeignKeyField, IntegerField, db_ref

class Session(BaseModel):
    id = CharField(primary_key=True, max_length=256)

class Point(BaseModel):
    id = AutoField()
    latitude = FloatField()
    longitude = FloatField()
    step = IntegerField()
    session = ForeignKeyField(Session, backref='points')


class Statistics(BaseModel):
    id = AutoField()
    session = ForeignKeyField(Session, backref='statistics')
    s3_reference = CharField(max_length=256)


class Embedding(BaseModel):
    id = AutoField()
    s3_reference = CharField(max_length=256)
    step = IntegerField()
    session = ForeignKeyField(Session, backref='embeddings')


class YOLOResult(BaseModel):
    id = AutoField()
    s3_reference = CharField(max_length=256)
    step = IntegerField()
    session = ForeignKeyField(Session, backref='embeddings')


db_ref.create_tables([Session, Point, Statistics, Embedding, YOLOResult])