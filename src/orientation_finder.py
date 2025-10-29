import pandas as pd
import osmnx as ox
from geopy.geocoders import Nominatim
from shapely.geometry import LineString
import math
import time
import os


# Setup paths relative to script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input and output files
input_file = os.path.join(script_dir, "../data/sample_addresses.csv")
output_folder = os.path.join(script_dir, "../output")
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "property_orientations.csv")


# Initialize geolocator
geolocator = Nominatim(user_agent="orientation_finder")


# Helper functions
def get_coords(address):
    """Get latitude and longitude for a given address."""
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Geocoding failed for {address}: {e}")
    return None


def get_nearest_road_bearing(lat, lon):
    """Find the nearest road and estimate its bearing."""
    try:
        G = ox.graph_from_point((lat, lon), dist=150, network_type="drive")
        edges = ox.graph_to_gdfs(G, nodes=False)
        nearest_edge = edges.iloc[0]
        geom = nearest_edge.geometry

        if isinstance(geom, LineString):
            x1, y1 = geom.coords[0]
            x2, y2 = geom.coords[-1]
            angle = math.degrees(math.atan2(x2 - x1, y2 - y1))
            bearing = (angle + 360) % 360
            return bearing
    except Exception as e:
        print(f"Road bearing failed at ({lat}, {lon}): {e}")
    return None


def bearing_to_orientation(bearing):
    """Convert numeric bearing to compass direction."""
    directions = [
        "North",
        "North-East",
        "East",
        "South-East",
        "South",
        "South-West",
        "West",
        "North-West",
    ]
    idx = round(bearing / 45) % 8
    return directions[idx]


# Main script
if not os.path.exists(input_file):
    print("Input file not found:", input_file)
    exit()

# Load input addresses
df = pd.read_csv(input_file)

results = []

for address in df["Address"]:
    coords = get_coords(address)
    if coords:
        lat, lon = coords
        bearing = get_nearest_road_bearing(lat, lon)
        if bearing is not None:
            orientation = bearing_to_orientation(bearing)
        else:
            orientation = "Unknown"
    else:
        orientation = "Not Found"

    results.append((address, orientation))
    time.sleep(1)  # Respect API rate limits

# Save output CSV
df_out = pd.DataFrame(results, columns=["Address", "Orientation"])
df_out.to_csv(output_file, index=False)

print("Orientation estimation complete. Output saved to:", output_file)
print(df_out)
