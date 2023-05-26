from fastapi import FastAPI, UploadFile, File
import uvicorn
import pathlib
import os
from api.construction import ConstructionAPI
from api.twogis import TwoGISAPI
from database.communication import DatabaseCommunication

app = FastAPI()

# Example data storage for construction site information
construction_site_data = []

# Example data storage for calculated statistics
statistics_data = {}

construction_api = ConstructionAPI()
twogis_api = TwoGISAPI()
database_communication = DatabaseCommunication()

@app.post('/api/upload-video')
def upload_video_file(video: UploadFile = File(...)):
    video_path = f"{video.filename}"
    with open(video_path, "wb") as file:
        file.write(video.file.read())

    # Retrieve video parameters
    file_size = video.file.seek(0, os.SEEK_END)
    file_name = video.filename
    file_format = pathlib.Path(file_name).suffix

    # Process the video and extract additional parameters if needed

    # Prepare the data to be sent to the other server
    data = {
        'video': open(video_path, 'rb')
    }

    # Return the video parameters
    return {
        'file_name': file_name,
        'file_size': file_size,
        'file_format': file_format
        # Include additional parameters as needed
    }

@app.post('/api/detect-location')
def receive_construction_site_data(data: dict):
    construction_site_data.append(data)
    return {'message': 'Construction site data received successfully'}

@app.get('/api/statistics')
def get_statistics():
    # Perform calculations or analysis on the stored data
    # ...
    # Code for calculating statistics

    # Populate the checkerboard or any suitable data structure with the calculated statistics
    # ...
    # Code to populate the checkerboard

    # Return the populated checkerboard or statistics
    return statistics_data

# Error handling and logging can be implemented using appropriate FastAPI features and libraries

# Test cases can be written to verify the functionality of different components

# Deployment can be done to a server or cloud platform following FastAPI's deployment guidelines

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
