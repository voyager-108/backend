import requests
import json
from api.construction import ConstructionAPI
from shapely.geometry import Polygon
from shapely.geometry import mapping

class TwoGisApi:
    
    """
    
	We use this class in order to get the following information: 
    
    1) Understanding which project, is the closest and returning the list of top 5 closest projects.
    2) If we already understood which project is the closest, then we need to understand which building is the closest. 
    3) When we understood, what building is the closest, we need to understand which section is the closest. 
    4) When we undertood, what section is the closest, we need to understand what floor and what flat is the closest. 
    
    In order to understand this point you have to use, polygon extraction, in order to check wether the current coordinates 
    belong to this specific polygon. And if they do indeed belong to it, then we'll have to work with it. 
    
    
    """
    
    def __init__(self):
        self.api_key = "e1fa047d-f2cd-4315-a7b5-140256c78b74"

    def extract_shapefile(self):
        # Read the JSON file
        with open('response.json', 'r') as file:
            data = json.load(file)

        # Get the polygon coordinates from the JSON data
        polygon_coords = data['result']['items'][0]['geometry']['hover']

        print("Here are the polygon coords:\n" + polygon_coords + "\n-----------------------\n")
        # Create a Shapely polygon object
        polygon = Polygon([tuple(map(float, coord.split())) for coord in polygon_coords.strip('POLYGON((').strip('))').split(',')])

        # Create a GeoJSON-like dictionary
        geojson_dict = {
            'type': 'Feature',
            'properties': {},
            'geometry': mapping(polygon)
        }

        # Write the GeoJSON dictionary to a file
        with open('output.geojson', 'w') as file:
            json.dump(geojson_dict, file)
            
    def analyze_coordinates(self):
        # API endpoint
        url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={self.latitude},{self.longitude}&fields=items.point,items.geometry.hover&sort_point={self.longitude}%2C{self.latitude}&sort=distance&key={self.api_key}"

        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Save the response to a JSON file
            with open("response.json", "w") as file:
                json.dump(data, file)

            print("Response saved to response.json")
        else:
            print("Error occurred:", response.status_code)