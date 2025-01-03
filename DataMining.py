import pandas as pd
import csv

# This file is a mess of the various functions I used to collect the necessary csv's of lat/lon data



'''
coord_list = ["LATITUDE","LONGITUDE"]
bus_df=pd.read_csv("data/Grand_Rapids_Bus_Stops.csv")

bus_df_cleaned = bus_df.dropna(subset=coord_list)
bus_coords = bus_df_cleaned[coord_list]
bus_coord_arr = bus_coords.values.tolist()

with open('data/bus_cleaned_coords.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(bus_coord_arr)
'''



'''
coord_list = ["Y", "X"]
protestant_df = pd.read_csv("data/protestant_churches.csv")

protestant_df_cleaned = protestant_df.dropna(subset=coord_list)
protestant_coords = protestant_df_cleaned[coord_list]
protestant_coord_arr = protestant_coords.values.tolist()

with open('data/protestant_cleaned_coords.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(protestant_coord_arr)
'''



'''
coord_list = ["latitude", "longitude"]
school_df = pd.read_csv("data/school_messy_coords.csv")

school_df_cleaned = school_df.dropna(subset=coord_list)
school_coords = school_df_cleaned[coord_list]
school_coord_arr = school_coords.values.tolist()

with open('data/school_cleaned_coords.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(school_coord_arr)
'''

import csv
import xml.etree.ElementTree as ET


def clean_csv(messy_coords):
    unique_coords = []
    for coord in messy_coords:
        is_unique = True
        for existing_coord in unique_coords:
            if ((float(coord[0]) - float(existing_coord[0])) ** 2 + (float(coord[1]) - float(existing_coord[1])) ** 2) ** 0.5 <= .005:
                is_unique = False
                break
        if is_unique:
            unique_coords.append(coord)

    return unique_coords


def kml_to_csv(kml_file):
    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # Find all coordinates
    coordinates = []
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        coordinates_element = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates')
        if coordinates_element is not None:
            coordinates_str = coordinates_element.text.strip()
            coordinates.extend(coordinates_str.split())

    coordinates = [coord.split(',') for coord in coordinates]
    parsed_coords = clean_csv(coordinates)

    # Write coordinates to CSV
    csv_file = "data/cleaned_" + kml_file.split('/')[-1].replace('.kml', '.csv')
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for lat, lon in parsed_coords:
            writer.writerow([float(lon), float(lat)])

    print(f"CSV file saved as: {csv_file}")

# Example usage
kml_file = "data/social_facilities.kml"
kml_to_csv(kml_file)

