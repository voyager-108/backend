import requests

class ConstructionSiteAPI:
    def __init__(self, api_url):
        self.api_url = api_url
        self.projects = []

    def fetch_projects(self):
        response = requests.get(self.api_url)
        data = response.json()

        self.projects = []
        for project in data:
            project_data = {
                "pk": project["pk"],
                "name": project["name"],
                "ref_id": project["ref_id"],
                "slug": project["slug"],
                "coords": project["coords"]
            }
            self.projects.append(project_data)

    def get_project_info(self):
        for project in self.projects:
            print("Project ID:", project["pk"])
            print("Project Name:", project["name"])
            print("Reference ID:", project["ref_id"])
            print("Slug:", project["slug"])
            print("Coordinates:", project["coords"])
            print("----------------------------------------")

    # Extend the class with additional methods to access more information
    # For example, to get building sections, floors, and flats information
    def get_building_sections(self, project_id):
        # Implement logic to fetch and return building sections data
        pass

    def get_floors(self, section_id):
        # Implement logic to fetch and return floors data
        pass

    def get_flats(self, floor_id):
        # Implement logic to fetch and return flats data
        pass

# Create an instance of ConstructionSiteAPI
api = ConstructionSiteAPI("https://samolet.ru/api_redesign/projects")

# Fetch projects data
api.fetch_projects()

# Access and print project information
api.get_project_info()

# Example usage of additional methods
# api.get_building_sections(project_id)
# api.get_floors(section_id)
# api.get_flats(floor_id)
