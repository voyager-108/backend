import requests
from construction import ConstructionAPI

# Create an instance of ConstructionAPI
api = ConstructionAPI()

api.fetch_projects()

print("Projects, were fetched.")

# Fetch projects from the API
api.fetch_project_info()

# # Get project information
api.print_all()


# # Get building sections for a project
# building_sections = api.get_building_sections(project_id=1)

# # Get floors for a building section
# floors = api.get_floors(section_id=1)

# # Get flats for a floor
# flats = api.get_flats(floor_id=1)
