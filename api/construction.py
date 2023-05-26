import requests

class ConstructionAPI:
    
    """

    Suppose I have a client app, that uses this api.

    1) At first, it gets a list of all projects separately, 
       after it chooses the project, depending on it's coordinates.

    2) When client choose a project, it has to be able to query this 
       project separately. 

    3) After getting the building, it should be able to query the 
       section. Next to that buildings.
        
        [Buildings] 
        -> [Sections of Buildings ] 
            -> [ Floors of Sections of Buildings]
                -> [ Flat of Floors of Sections of Buildings ]
                
    """

    def __init__(self):
        self.projects = []

    def fetch_projects(self):
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

    def fetch_projects_info(self):
        
        for project in self.projects:

            buildings = self.fetch_buildings(project["slug"])
            
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
                project["buildings"].append(building_data)

    def fetch_project_info(self, slug):
        
        if len(self.projects) == 0:
            self.fetch_projects()
        
        return 0;

    def fetch_buildings(self, slug):

        url = f"https://samolet.ru/api_redesign/projects_buildings/{slug}/flats"
        response = requests.get(url)
        data = response.json()
        return data

    def fetch_floors(self, section_id):

        url = f"https://samolet.ru/api_redesign/sections_floors/{section_id}/flats"
        response = requests.get(url)
        data = response.json()
        return data

    def fetch_flats(self, floor_id):

        url = f"https://samolet.ru/api_redesign/floors_properties/{floor_id}/flats/"
        response = requests.get(url)
        data = response.json()
        return data
        
    def fetch_flat_info(self, flat_id):
        url = f"https://samolet.ru/api_redesign/flats/{flat_id}/"
        response = requests.get(url)
        data = response.json()
        return data

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

