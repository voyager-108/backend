import random
import folium
import math
from scipy.spatial import ConvexHull

def generate_random_points(center_lat, center_lng, radius, num_points):
    points = []
    for _ in range(num_points):
        # Generate random bearing (in degrees)
        bearing = random.uniform(0, 360)

        # Generate random distance within the radius
        distance = random.uniform(0, radius)

        # Convert distance to kilometers
        distance_km = distance / 1000.0

        # Calculate the new coordinates
        lat, lng = calculate_new_coordinates(center_lat, center_lng, distance_km, bearing)

        points.append([lat, lng])

    return points

def calculate_new_coordinates(lat, lng, distance, bearing):
    earth_radius = 6371.0  # Earth's radius in kilometers

    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lng_rad = math.radians(lng)
    bearing_rad = math.radians(bearing)

    # Calculate new latitude
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance / earth_radius) +
                            math.cos(lat_rad) * math.sin(distance / earth_radius) * math.cos(bearing_rad))
    new_lat = math.degrees(new_lat_rad)

    # Calculate new longitude
    new_lng_rad = lng_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance / earth_radius) * math.cos(lat_rad),
                                        math.cos(distance / earth_radius) - math.sin(lat_rad) * math.sin(new_lat_rad))
    new_lng = math.degrees(new_lng_rad)

    return new_lat, new_lng

# Center coordinates
center_lat = 37.7749  # San Francisco latitude
center_lng = -122.4194  # San Francisco longitude

# Radius in meters
radius = 1000

# Number of random points
num_points = 50

# Generate random points
points = generate_random_points(center_lat, center_lng, radius, num_points)

# Create a Folium map centered on the specified coordinates
map_center = [center_lat, center_lng]
m = folium.Map(location=map_center, zoom_start=13)

# Add markers for each point
for point in points:
    folium.Marker(location=point).add_to(m)

# Find the convex hull of the points using QuickHull algorithm
hull = ConvexHull(points)
hull_points = [points[i] for i in hull.vertices]

# Draw the convex hull polygon
convex_hull_polygon = folium.Polygon(locations=hull_points, color='red', fill=True, fill_color='red', fill_opacity=0.4)
convex_hull_polygon.add_to(m)

# Save the map to an HTML file
m.save('map.html')
