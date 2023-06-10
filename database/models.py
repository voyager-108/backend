from database import BaseModel, CharField, AutoField, FloatField, ForeignKeyField, IntegerField, db_ref
from pydantic import BaseModel as PydanticBaseModel

class Session(BaseModel):
    id = CharField(primary_key=True, max_length=256)

class Point(BaseModel):
    id = AutoField()
    latitude = FloatField()
    longitude = FloatField()
    altitude = FloatField(null=True)
    accuracy = FloatField(null=True)
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


class SessionLocationReference(BaseModel):
    id = AutoField()
    session = ForeignKeyField(Session, backref='locations')
    project_slug = CharField(max_length=256, null=True)
    building_pk = IntegerField(null=True)
    section_id = IntegerField(null=True)
    floor_id = IntegerField(null=True)

    class Meta:
        class FastAPIModel(PydanticBaseModel):
            session: str
            project_slug: str = None
            building_pk: int = None
            section_id: int = None
            floor_id: int = None



db_ref.create_tables([Session, Point, Statistics, Embedding, YOLOResult, SessionLocationReference])