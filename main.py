from fastapi import FastAPI, UploadFile, File
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

# Example data storage for construction site information
construction_site_data = []

# Example data storage for calculated statistics
statistics_data = {}

construction_api = ConstructionAPI()
twogis_api = TwoGisApi()


@app.post('/api/upload-video')
def upload_video_file(video: UploadFile = File(...)):
    """
    This method is called every 5 seconds. It accepts the zipped video file and sends it to the ML server
    for processing. If it is the first video, it sends the video to the ML server and receives a hash name
    for the video. If it is not the first video, it keeps sending the video. If the video recording is interrupted
    on the client side, the client can access another endpoint stating that it is interrupted, and the hash is sent
    to the ML server to retrieve the results of the video analysis.
    """
    video_path = f"{video.filename}"
    with open(video_path, "wb") as file:
        file.write(video.file.read())

    # Retrieve video parameters
    file_size = video.file.seek(0, os.SEEK_END)
    file_name = video.filename
    file_format = pathlib.Path(file_name).suffix

    # Process the video and extract additional parameters if needed

    # Prepare the data to be sent to the ML server
    data = {'video': open(video_path, 'rb')}

    # Send the video to the ML server
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


@app.post('/api/detect-project')
def detect_project_location(data: dict):
    """
    This endpoint is called when a client opens the app
    and sends their location. Based on the information from the ConstructionAPI class,
    we need to return the top five projects that are closest to the person.
    """
    construction_site_data.append(data)
    return {'message': 'Construction site data received successfully'}


@app.post('/api/detect-section-location')
def detect_section_location(data: dict):
    """
    This endpoint is only called when we have already defined a specific project.
    We choose between each section using the ConstructionAPI class.
    """
    construction_site_data.append(data)
    return {'message': 'Construction site data received successfully'}


@app.post('/api/detect-flat-floor-location')
def detect_flat_floor_location(data: dict):
    """
    This endpoint is only called when we have already defined a specific project and section.
    We choose between each flat and floor using the ConstructionAPI class and TwoGISAPI class.
    """
    construction_site_data.append(data)
    return {'message': 'Construction site data received successfully'}


@app.get('/api/statistics')
def get_statistics():
    # Perform calculations or analysis on the stored data
    # ...
    # Code for calculating statistics

    # Populate the statistics_data with the calculated statistics
    # ...
    # Code to populate statistics_data

    # Return the populated statistics_data
    return statistics_data


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
