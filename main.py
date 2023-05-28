from fastapi import FastAPI, UploadFile, File
from typing import List
import uvicorn
import pathlib
import os
import sys
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.construction import ConstructionAPI
from api.twogis import TwoGisApi
from database.communication import DatabaseCommunication

app = FastAPI()

construction_api = ConstructionAPI()
construction_api.fetch_projects()

class LocationData:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        accuracy: float,
        altitude: float,
        speed: float,
        speedAccuracy: float,
        heading: float,
        time: float,
        isMock: bool
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.accuracy = accuracy
        self.altitude = altitude
        self.speed = speed
        self.speedAccuracy = speedAccuracy
        self.heading = heading
        self.time = time
        self.isMock = isMock
        

@app.post('/api/location-section')
def propose_section(coordinates: list):
    """
    This function accepts coordinates and detects the closest project.
    returns a project, buildings, sections.
    """

    construction_api.fetch_closest_project(coordinates)
    print("Fetched the projects!\n")
    construction_api.fetch_project_building_info()
    print("Fetched the buildings!\n")
    proposed_section = construction_api.fetch_building_section_info()
    print("Fetched the sections!\n")
    # Perform the logic to detect the section based on the coordinates
    # ...
    # Code for detecting the section

    # Return the detected section
    return {'section': proposed_section}


@app.post('/api/select-section')
def select_section(section: str):
    """
    This function accepts a section id, chooses this section, and returns details about this section.
    returns: number of floors, number of flats.
    """
    # Store the selected section in the construction_site_data or perform any necessary logic
    # ...
    # Code for selecting the section

    # Return a success message
    return {'message': 'Section selected successfully'}


@app.post('/api/calculate-floor')
def pick_location(coordinates: list):
    """
    This function accepts geolocation, and returns the calculated floor.
    """
    # Perform the logic to calculate the floor based on the coordinates
    # ...
    # Code for calculating the floor

    # Return the calculated floor
    calculated_floor = 0
    return {'floor': calculated_floor}

@app.post('/api/upload-video')
def upload_video_file(video: UploadFile, locations: List[LocationData]):
    video_path = f"{video.filename}"
    with open(video_path, "wb") as file:
        file.write(video.file.read())

    # Retrieve video parameters
    file_size = video.file.seek(0, pathlib.SEEK_END)
    file_name = video.filename
    file_format = pathlib.Path(file_name).suffix

    # Prepare the location data
    location_data = []
    for location in locations:
        location_info = {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'accuracy': location.accuracy,
            'altitude': location.altitude,
            'speed': location.speed,
            'speedAccuracy': location.speedAccuracy,
            'heading': location.heading,
            'time': location.time,
            'isMock': location.isMock
        }
        location_data.append(location_info)

    # Prepare the data to be sent to the ML server
    data = {'video': open(video_path, 'rb'), 'locations': location_data}

    # Send the video and location data to the ML server
    response = requests.post("ML_SERVER_URL", files=data)

    # Handle the response from the ML server
    if response.status_code == 200:
        # Video processing successful
        result = response.json()
        video_hash = result.get('video_hash')  # Retrieve the video hash from the response
        # Additional processing or storing of the video hash can be done here

        # Return the video parameters and video hash
        return {
            'file_name': file_name,
            'file_size': file_size,
            'file_format': file_format,
            'video_hash': video_hash
            # Include additional parameters as needed
        }
    else:
        # Video processing failed
        # Handle the error or return an appropriate response
        return {'message': 'Video processing failed'}
    
@app.get('/api/statistics')
def get_statistics(project_slug: str):
    """
    This function accepts a project's slug and returns all the available statistics from the db. 
    """
    # Perform calculations or analysis on the stored data
    # ...
    # Code for calculating statistics

    # Populate the statistics_data with the calculated statistics
    # ...
    # Code to populate statistics_data

    # Return the populated statistics_data
    statistics_data = 1
    return statistics_data


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8090)
