import uuid
import uvicorn
import json
import os
import sys
import requests
import folium
import aiohttp
import logging

from typing import Annotated, List
from scipy.spatial import ConvexHull
from fastapi import FastAPI, HTTPException, UploadFile, File, Body

from database.utils import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.construction import construction_api
from api.twogis import TwoGisApi
from database.communication import DatabaseCommunication


from models import *

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.samolet import router as samolet_router

app.router.include_router(samolet_router)


reference_altitude = None  # Global variable to store the reference altitude

logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
handler =logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] :: %(message)s'))
logger.addHandler(handler)



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
async def process_video( 
        video: UploadFile = File(...),
        locations: list[LocationInfo] = [],
        session: Annotated[str, Body(embed=True)] = None,
        final: Annotated[bool, Body(embed=True)] = False
    ):
    """
    This function accepts a video file and a list of position information.
    It processes the video and position data.
    """
    logger.info(f'[v2] Video: ({video.filename}). Session: ({session})')

    video = video
    session = session or uuid.uuid4().hex

    save_session(session)

    video_path = f"{video.filename}"
    with open(video_path, "wb") as file:
        file.write(await video.read())

    data = {
        'video': open(video_path, 'rb'),
    }

    if final:
        logger.info(f'[v2] Finalizing session: ({session})')

        embeddings = get_embeddings(session)
        yolo_results = get_yolo_results(session)

        logger.info(f'[v2] Total num. of embeddings: ({len(embeddings)}), YOLOv8 results: ({len(yolo_results)})')

        data['embeddings'] = [embedding.s3_reference for embedding in embeddings]
        data['yolo_results'] = [yolo_result.s3_reference for yolo_result in yolo_results]
        data['isLast'] = True
    

    compute_request = aiohttp.FormData()

    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                compute_request.add_field(key, item)
        elif isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
            compute_request.add_field(key, str(value))
        else:
            compute_request.add_field(key, value)

    async with aiohttp.ClientSession() as client:
        response = client.post("http://178.170.197.93:7080/score-card/v2/video", data=compute_request)

        # response = requests.post("http://178.170.197.93:7080/score-card/video", files=data)
        # Prepare the location data

        # @teexone: I think this is not needed anymore
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        location_data = []
        for location in locations:
            location_info = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'accuracy': location.accuracy,
                'altitude': location.altitude,
            }
            location_data.append(location_info)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # @teexone: I think this is not needed anymore

        save_locations(session, locations)

        # Send the video to the ML server

        # Handle the response from the ML server

        async with response as r:
            if r.ok:
                # Video processing successful
                result = await r.json()
                # Additional processing or storing of the video hash can be done here

                # Save the result as JSON in output.json
                with open('output.json', 'w') as output_file:
                    json.dump(result, output_file)

                if final:
                    logger.info(f'[v2] Result from processing server. Finalized session: ({session})')
                    return await r.json()
                
                else:
                    logger.info(f'[v2] Result from processing server. Session: ({session}). Embeddings: ({result["embeddings"]}). '
                                f'YOLOv8 results: ({result["yolo"]})')
                    
                    db_embed = save_embeddings(session, result['embeddings'])
                    db_yolo = save_yolo_results(session, result['yolo'])

                    logger.info(f'[v2] Saved embeddings and YOLOv8 results. Session: ({session}). '
                                f' Embeddings [id= {db_embed.id}]. YOLOv8 results: [id= {db_yolo.id}]')
                    
                # Return the video hash.
                return {"session": session}


            else:
                HTTPException(r.status, r.reason)
        
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
