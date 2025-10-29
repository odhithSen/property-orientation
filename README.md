# 🧭 Australian Property Orientation Finder

### Overview
This project estimates the orientation of Australian residential properties using open-source geospatial data.
Each property’s address is geocoded using OpenStreetMap’s Nominatim API to obtain coordinates, and nearby road
geometry is analyzed with OSMnx to infer which direction the property faces.

### Steps
1. Geocode address to get latitude and longitude (via Nominatim API).
2. Retrieve nearby road network within 50m using OSMnx.
3. Calculate the bearing of the nearest road segment.
4. Map the bearing to compass directions (N, NE, E, SE, S, SW, W, NW).
5. Export the final output (address + orientation) to a CSV file.

### Technologies Used
- Python
- Pandas
- OSMnx
- Geopy
- Shapely

### Usage
```bash
pip install -r requirements.txt
python src/orientation_finder.py