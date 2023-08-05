import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance


def parse_coordinate_range():
    
    # read in the file of coordinates
    with open("DatabasePrograms/nz_land_coordinates.txt", 'r') as f:
        coord_str = f.read()
        
    # Split the string by line breaks to get each line
    lines = coord_str.strip().split('\n')

    # Initialize an empty list to store coordinate pairs
    coordinates = []

    # Iterate through each line and split by "- " to get start and end coordinates
    # Iterate through each line and split by "- " to get start and end coordinates
    for line in lines:
        start_str, end_str = line.split(" - ")
        start = tuple(map(int, start_str.strip("()").split(", ")))
        end = tuple(map(int, end_str.strip("()").split(", ")))

        # Extract all coordinates between the start and end ranges
        for lat in range(start[0], end[0] - 1, -1):
            for lon in range(start[1], end[1] + 1):
                print((lat, lon))
                coordinates.append((lat, lon))

    return coordinates

def generate_probability_map():
    # Define the latitude and longitude ranges
    lat_range = range(-53, -14)
    lon_range = range(150, 201)

    # Create a meshgrid of latitude and longitude
    lon, lat = np.meshgrid(lon_range, lat_range)

    # Initialize a probability map with all ones and convert it to float64
    probability_map = np.ones_like(lat, dtype=np.float64)

    # Set the probability to 0 for points within the New Zealand landmass
    nz_land_coordinates = parse_coordinate_range()
    
    # add a coordinate to the list of land coordinates
    nz_land_coordinates.append((-44, 184))

        # Iterate through the meshgrid and calculate the distance to the nearest land coordinate
    for i, lat_coord in enumerate(lat_range):
        for j, lon_coord in enumerate(lon_range):
            min_dist = min(distance.euclidean((lat_coord, lon_coord), land_coord) for land_coord in nz_land_coordinates)
            
            # Use an exponential decay function to scale the probability based on distance to land
            probability_map[i, j] = np.exp(-min_dist / 0.5) # Adjust the denominator to control the decay rate

    for lat_coord, lon_coord in nz_land_coordinates:
        # Check if the coordinates fall within the expected range
        if lat_coord >= min(lat_range) and lat_coord <= max(lat_range) and lon_coord >= min(lon_range) and lon_coord <= max(lon_range):
            lat_index = lat_coord - min(lat_range)
            lon_index = lon_coord - min(lon_range)
            probability_map[lat_index, lon_index] = 0
            

            
    # Normalize the probability map to have the highest probability near the coastline
    probability_map /= probability_map.max()

    return lat, lon, probability_map

# Generate the probability map
lat, lon, probability_map = generate_probability_map()
np.save('DatabasePrograms/probability_map.npy', probability_map)


# Plot the probability map
plt.figure(figsize=(10, 10))
plt.imshow(probability_map, extent=(150, 200, -53, -15), cmap='hot', origin='lower', alpha=0.7)
plt.colorbar(label='Probability')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Probability Map for New Zealand Coastline')
plt.grid()
plt.show()

