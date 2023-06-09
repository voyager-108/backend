from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from typing import List
import uvicorn
import json
import pathlib
import os
import sys
import requests
import random
import folium
import math
from scipy.spatial import ConvexHull

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.construction import ConstructionAPI
from api.twogis import TwoGisApi
from database.communication import DatabaseCommunication

app = FastAPI()


construction_api = ConstructionAPI()
construction_api.fetch_projects()

reference_altitude = None  # Global variable to store the reference altitude

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
    video_file: UploadFile
    positions: List[LocationInfo]

def generate_polygon(request: VideoProcessingRequest):
    # Get the positions from the request
    positions = request.positions

    # Extract latitude and longitude values from positions
    points = [[position.latitude, position.longitude] for position in positions]

    # Create a Folium map centered on the first position
    map_center = [positions[0].latitude, positions[0].longitude]
    m = folium.Map(location=map_center, zoom_start=13)

    # Add markers for each point
    for point in points:
        folium.Marker(location=point).add_to(m)

    # Find the convex hull of the points using the QuickHull algorithm
    hull = ConvexHull(points)
    hull_points = [points[i] for i in hull.vertices]

    # Draw the convex hull polygon
    convex_hull_polygon = folium.Polygon(locations=hull_points, color='red', fill=True, fill_color='red', fill_opacity=0.4)
    convex_hull_polygon.add_to(m)

    # Save the map to an HTML file
    m.save('map.html')

    return hull_points

@app.post('/api/location-section')
def propose_section(coordinates: Coordinates):

    """
    This function accepts coordinates and detects the closest project.
    returns a project, buildings, sections.
    """

    construction_api.fetch_closest_project(coordinates.coordinates)
    print("Fetched the projects!\n")
    construction_api.fetch_project_building_info()
    print("Fetched the buildings!\n")
    proposed_section = construction_api.fetch_building_section_info()
    print("Fetched the sections!\n")
    
    return proposed_section

@app.post('/api/select-section')
def select_section(request: SelectSectionRequest):
    """
    This function accepts a section id, chooses this section, and returns details about this section.
    returns: number of floors, number of flats.
    """
    
    project_slug = request.project_slug
    building_pk = request.building_pk
    section_id = request.section_id

    url = f"https://samolet.ru/api_redesign/sections_floors/{section_id}/flats/facets"
    response = requests.get(url)
    data = response.json()

    rooms_list = data['facets']['rooms']
    number_of_rooms = len(rooms_list)

    # Extract the number of floors
    number_of_floors = data['count_floors']

    # Return a success message
    # number of floors. number of flats per floor.  
    return {'floors': number_of_floors, "flats" : number_of_rooms}

@app.post('/api/calculate-floor')
def select_floor(request: AltitudeRequest):
    global reference_altitude  # Access the global variable

    if reference_altitude is None:
        # Set the reference altitude for the ground floor
        reference_altitude = request.altitude

    # Calculate the floor based on the altitude relative to the reference altitude
    calculated_floor = int((request.altitude - reference_altitude) // 3) + 1

    return {'floor': calculated_floor}

@app.post('/api/process-video')
async def process_video(request: VideoProcessingRequest):
    """
    This function accepts a video file and a list of position information.
    It processes the video and position data.
    """
    video = request.video
    locations = request.locations

    video_path = f"{video.filename}"
    with open(video_path, "wb") as file:
        file.write(await video.read())

    data = {'video': open(video_path, 'rb')}

    # Prepare the location data
    location_data = []
    for location in locations:
        location_info = {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'accuracy': location.accuracy,
            'altitude': location.altitude,
        }
        location_data.append(location_info)

    # Send the video to the ML server
    response = requests.post("http://voyager108.ru:7080", files=data)

    # Handle the response from the ML server
    if response.status_code == 200:
        # Video processing successful
        result = response.json()
        print("Successful!")  # Retrieve the video hash from the response
        # Additional processing or storing of the video hash can be done here

        # Save the result as JSON in output.json
        with open('output.json', 'w') as output_file:
            json.dump(result, output_file)

        # Return the video hash.
        return {'video_hash': "success"}
    else:
        # Video processing failed
        # Handle the error or return an appropriate response
        return {'message': 'Video processing failed'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
