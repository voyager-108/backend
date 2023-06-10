from typing import Iterable
import peewee
from database.models import *
from models import LocationInfo


def save_locations(session: str, locations: list[LocationInfo]):
    # Save the locations to the database
    for step, location in enumerate(locations):
        Point.create(
            latitude=location.latitude,
            longitude=location.longitude,
            altitude=location.altitude,
            accuracy=location.accuracy,
            step=step,
            session=session
        )


def save_session(session: str):
    # Save the session to the database
    return Session.get_or_create(id=session)[0]


def save_embeddings(session: str, embeddings: str):
    step = Embedding.select().where(Embedding.session == session).count()  

    # Save the embeddings to the database
    return Embedding.create(
        s3_reference=embeddings,
        step=step,
        session=session
    )


def save_yolo_results(session: str, yolo_result: str):
    step = YOLOResult.select().where(YOLOResult.session == session).count()

    # Save the yolo results to the database
    return YOLOResult.create(
        s3_reference=yolo_result,
        step=step,
        session=session
    )


def get_embeddings(session: str) -> Iterable[Embedding]:
    # Get the embeddings from the database
    return Embedding.select().where(Embedding.session == session).order_by(Embedding.step)

def get_yolo_results(session: str) -> Iterable[YOLOResult]:
    # Get the yolo results from the database
    return YOLOResult.select().where(YOLOResult.session == session).order_by(YOLOResult.step)