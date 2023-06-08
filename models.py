from fastapi import File, UploadFile
from pydantic import BaseModel


class Coordinates(BaseModel):
    coordinates: list[float]

class SelectSectionRequest(BaseModel):
    project_slug: str
    building_pk: str
    section_id: str

class AltitudeRequest(BaseModel):
    altitude: float

class LocationInfo(BaseModel):
    latitude: float
    longitude: float
    accuracy: float
    altitude: float

class VideoProcessingRequest(BaseModel):
    video_file: UploadFile = File(...)
    positions: list[LocationInfo] = []
    embedding: list[str] = []
    yolo_results: list[str] = []
    session: str = None
    final: bool = False