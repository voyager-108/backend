from fastapi.routing import APIRouter
from api.construction import construction_api

router = APIRouter(
    prefix="/samolet",
)



@router.get("/fetchAllProjects")
async def fetchAllProjects():
    """
    This function fetches all projects from the API.
    """
    return construction_api.projects if construction_api.projects else construction_api.fetch_projects()

@router.get("/fetchAllBuildings")
async def fetchAllBuildings(slug: str):
    """
    This function fetches all buildings from the API.
    """
    response = construction_api.fetch_buildings(slug=slug)
    buildings = response.result()
    buildings = construction_api.unwind_buildings_list(buildings)

    return_buildings = {}

    for key, building in buildings.items():
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

        return_buildings[key] = building_data
    return return_buildings

@router.get("/fetchAllSections")
async def fetchAllSections(building_pk: str):
    """
    This function fetches all sections from the API.
    """
    sections = construction_api.fetch_sections(building_pk=building_pk).result()
    return_sections = []
    for section in sections:
        return_sections.append({
            "id": section["id"],
            "plan": section["plan"],
            "point": section["point"],
            "hover": section["hover"],
            "number": section["number"],
            "total_count": section["total_count"],
        })

    return return_sections


# # Should be implented in the future
# # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# @router.get("/fetchAllFloors")
# async def fetchAllFloors(section_id: str):
#     """
#     This function fetches all floors from the API.
#     """
#     floors = construction_api.fetch_floors(section_id=section_id).result()
#     return_floors = []
#     for floor in floors:
#         return_floors.append({
#             "id": floor["id"],
#             "plan": floor["plan"],
#             "point": floor["point"],
#             "hover": floor["hover"],
#             "number": floor["number"],
#             "miniplan": floor["miniplan"],
#             "flats_url": floor["flats_url"],
#             "has_flats": floor["has_flats"],
#             "total_count": floor["total_count"],
#             "miniplan_hover": floor["miniplan_hover"]
#         })

#     return return_floors
# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# @router.get("/fetchAllFlats")
# async def fetchAllFlats(flat_d: str):
#     """
#     This function fetches all flats from the API.
#     """
#     return construction_api.fetch_flats(flat_id=flat_d).result()


