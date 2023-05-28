import random
import folium
import math
from scipy.spatial import ConvexHull
from typing import List
from pydantic import BaseModel

class LocationInfo(BaseModel):
    latitude: float
    longitude: float
    accuracy: float
    altitude: float

class VideoProcessingRequest(BaseModel):
    video_file: str
    positions: List[LocationInfo]

# Create a sample VideoProcessingRequest instance
request = VideoProcessingRequest(
    video_file='sample_video.mp4',
    positions=[
        LocationInfo(latitude=37.7749, longitude=-122.4194, accuracy=10.0, altitude=0.0),
        LocationInfo(latitude=37.7745, longitude=-122.4189, accuracy=10.0, altitude=0.0),
        LocationInfo(latitude=37.7738, longitude=-122.4192, accuracy=10.0, altitude=0.0),
        LocationInfo(latitude=37.7741, longitude=-122.4200, accuracy=10.0, altitude=0.0),
    ]
)

# Generate the polygon for the positions in the request
polygon_points = generate_polygon(request)

# Print the points that generate the polygon
print("Polygon Points:")
for point in polygon_points:
    print(point)
