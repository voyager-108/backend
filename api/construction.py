import requests
from geopy.distance import geodesic

class ConstructionAPI:

    """
    TODO: complete the description of what the class does. 
    """

    def __init__(self):
        self.projects = []
        self.current_project = None
        self.current_building = None
        self.current_section = None

    """
    Main fetching functions, that also fill up private attributes. 
    """

    def fetch_projects(self):

        """
        We use this function in order to fetch new information about the projects.
        Everytime we start a new instance of this class, we call it so we can fill our 
        self.projects list.
        """
        response = requests.get("https://samolet.ru/api_redesign/projects/")
        data = response.json()

        self.projects = []
        for project in data:
            project_data = {
                "id": project["pk"],
                "name": project["name"],
                "ref_id": project["ref_id"],
                "slug": project["slug"],
                "coords": project["coords"],
                "buildings": []
            }
            self.projects.append(project_data)

        return self.projects

    def fetch_project_building_info(self):

        buildings = self.fetch_buildings(self.current_project["slug"])
        
        for building in buildings:
            building_data = {
                    "pk": building["pk"],
                    "name": building["name"],
                    "hover": building["hover"],
                    "plan": building["plan"],
                    "number": building["number"],
                    "readiness": building["readiness"],
                    "free_count": building["free_count"],
                    "book_count": building["book_count"],
                    "shield_top": building["shield_top"],
                    "sections_set": building["section_set"],
                    "sections" : []
                }
            self.current_project["buildings"].append(building_data)
        
        return self.current_project

    def fetch_building_section_info(self):
        
        i = 0
        for building in self.current_project["buildings"]:
            
            sections = self.fetch_sections(building["pk"])

            self.current_project["buildings"][i]["sections"] = []

            for section in sections:
                print(section)
                section_data = {
                    "id": section["id"],
                    "plan": section["plan"],
                    "point": section["point"],
                    "hover": section["hover"],
                    "number": section["number"],
                    "total_count": section["total_count"],
                    "floors": []
                }
                self.current_project["buildings"][i]["sections"].append(section_data)
            
            self.current_project["buildings"][i]["sections"].sort(key=lambda x: x["number"]) # sort buildings by "number"

            i+=1
            
        return self.current_project
        
    def fetch_section_floor_info(self, section):
        floors = self.fetch_floors(section["id"])

        section["floors"] = []  # Clear the existing floors before adding new ones

        for floor in floors:
            floor_data = {
                "id": floor["id"],
                "plan": floor["plan"],
                "point": floor["point"],
                "hover": floor["hover"],
                "number": floor["number"],
                "miniplan": floor["miniplan"],
                "flats_url": floor["flats_url"],
                "has_flats": floor["has_flats"],
                "total_count": floor["total_count"],
                "miniplan_hover": floor["miniplan_hover"]
            }
            section["floors"].append(floor_data)

        section["floors"].sort(key=lambda x: x["number"])  # Sort floors by "number"

    """
    Fetch closest, provide the closest location of said type.
    """

    def fetch_closest_project(self, coordinates):
            """
            Fetches the closest project based on the given coordinates.

            Args:
                coordinates (tuple): A tuple containing latitude and longitude coordinates.

            Returns:
                None or project.

            Example:
                >>> api = ConstructionAPI()
                >>> api.fetch_closest_project((51.5074, -0.1278))
                Closest project: Project Name, distance is 2.5 km
            """
            if not self.projects:
                self.fetch_projects()

            latitude, longitude = coordinates

            closest_project = None
            closest_distance = float("inf")

            for project in self.projects:
                project_coords = project["coords"]
                project_latitude, project_longitude = project_coords

                distance = geodesic((latitude, longitude), (project_latitude, project_longitude)).km

                if distance < closest_distance:
                    closest_distance = distance
                    closest_project = project

            if closest_project:
                self.current_project = closest_project
                self.current_building = None
                self.current_section = None
                closest_project["distance"] = closest_distance
                return closest_project
            else:
                print("No projects found.")

    def fetch_closest_building(self, coordinates):
        if self.current_project is None:
            self.fetch_closest_project()
        

        project_coords = self.current_project["coords"]
        project_latitude, project_longitude = project_coords

        if coordinates != project_coords:
            print("Coordinates do not match the selected project.")
            return

        buildings = self.fetch_buildings(self.current_project["slug"])

        closest_building = None
        closest_distance = float("inf")

        for building in buildings:
            building_coords = building["coords"]
            building_latitude, building_longitude = building_coords

            distance = geodesic((project_latitude, project_longitude), (building_latitude, building_longitude)).km

            if distance < closest_distance:
                closest_distance = distance
                closest_building = building

        if closest_building:
            self.current_building = closest_building
            self.current_section = None
            print("Closest building:", closest_building["name"])
        else:
            print("No buildings found.")

    def fetch_closest_section(self, coordinates):
            
            """

            TODO: 
            1) Unpack the coordinates
            2) If self.current_project == None, tell to pick the project. 
            3) If self.current_project is picked, extract coordinates from self.current_project. 
            4) Use extracted coordinates in order to call twogis api, and extract all the building in this project, that belong to "Samolet"
            5) Call fetch_closest_section providing the coordinates.

            """

            pass  

    """
    Fetch functions used to query the api
    """

    def fetch_buildings(self, slug):

        url = f"https://samolet.ru/api_redesign/projects_buildings/{slug}/flats"
        response = requests.get(url)
        data = response.json()
        return data

    def fetch_sections(self, building_pk):

        url = f"https://samolet.ru/api_redesign/buildings_sections/{building_pk}/flats/"
        response = requests.get(url)
        data = response.json()
        return data

    def fetch_floors(self, floor_id):

        url = f"https://samolet.ru/api_redesign/floors_properties/{floor_id}/flats/"
        response = requests.get(url)
        data = response.json()
        return data
        
    def fetch_flats(self, flat_id):
        url = f"https://samolet.ru/api_redesign/flats/{flat_id}/"
        response = requests.get(url)
        data = response.json()
        return data

    """
    Print functions, used to output current state
    """ 
          
    def print_project_info(self):
        for project in self.projects:
            print("Project ID:", project["id"])
            print("Project Name:", project["name"])
            print("Reference ID:", project["ref_id"])
            print("Slug:", project["slug"])
            latitude, longitude = project["coords"]
            print("Coordinates:", latitude, ",", longitude)
            print("----------------------------------------")

    def print_all(self):
        for project in self.projects:
            print("Project ID:", project["id"])
            print("Project Name:", project["name"])
            print("Reference ID:", project["ref_id"])
            print("Slug:", project["slug"])
            latitude, longitude = project["coords"]
            print("Coordinates:", latitude, ",", longitude)
            print("----------------------------------------")

            for building in project["buildings"]:
                print("Building ID:", building["pk"])
                print("Building Name:", building["name"])
                print("Building Hover:", building["hover"])
                print("Building Plan:", building["plan"])
                print("Building Number:", building["number"])
                print("Building Readiness:", building["readiness"])
                print("Building Free Count:", building["free_count"])
                print("Building Book Count:", building["book_count"])
                print("Building Shield Top:", building["shield_top"])
                print("Building Sections Set:", building["sections_set"])
                print("----------------------------------------")

                for section in building["sections"]:
                    print("Section ID:", section["id"])
                    print("Section Name:", section["name"])
                    print("Section Hover:", section["hover"])
                    print("Section Plan:", section["plan"])
                    print("Section Number:", section["number"])
                    print("----------------------------------------")

                    for floor in section["floors"]:
                        print("Floor ID:", floor["id"])
                        print("Floor Number:", floor["number"])
                        print("Floor Plan:", floor["plan"])
                        print("----------------------------------------")

                        for flat in floor["flats"]:
                            print("Flat ID:", flat["id"])
                            print("Flat Name:", flat["name"])
                            print("Flat Area:", flat["area"])
                            print("Flat Price:", flat["price"])
                            print("----------------------------------------")

