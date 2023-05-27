
import sys
import os
import requests

# Add the path to the 'api' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.construction import ConstructionAPI

# Create an instance of ConstructionAPI
api = ConstructionAPI()

api.fetch_projects()
print("Projects, were fetched.")

# Fetch projects from the API
api.print_project_info()


# # Get building sections for a project
# building_sections = api.get_building_sections(project_id=1)

# # Get floors for a building section
# floors = api.get_floors(section_id=1)

# # Get flats for a floor
# flats = api.get_flats(floor_id=1)
