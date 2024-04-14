import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import threading
import time

# Read the CSV file
df = pd.read_csv('FIR_Details_Data.csv')

# Creating an instance of Nominatim Class
geolocator = Nominatim(user_agent="my_request")

# Applying the rate limiter wrapper
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Dictionary to store already geocoded locations
geocoded_locations = {}

# Function to geocode location
def geocode_location(place):
    if place in geocoded_locations:
        return geocoded_locations[place]
    else:
        location = geocode(place)
        if location:
            geocoded_locations[place] = (location.latitude, location.longitude)
            return (location.latitude, location.longitude)
        else:
            return None

# Function to save DataFrame to CSV file
def save_to_csv():
    df.to_csv('FIR_Details_Data.csv', index=False)
    print("Data saved to 'FIR_Details_Data.csv'")

# Apply geocoding only if latitude and longitude are 0
for index, row in df.iterrows():
    if row['Latitude'] == 0 or row['Longitude'] == 0:
        location = geocode_location(row['Village_Area_Name'])
        if location:
            df.at[index, 'Latitude'] = location[0]
            df.at[index, 'Longitude'] = location[1]
            print(f"Geocoded: {row['Village_Area_Name']} - Latitude: {location[0]}, Longitude: {location[1]}")
        else:
            print(f"Geocoding failed for: {row['Village_Area_Name']}")

    # Save DataFrame to CSV file every 10 seconds
    if (index + 1) % 10 == 0:
        threading.Timer(10, save_to_csv).start()
        time.sleep(10)  # Sleep for 10 seconds to avoid overlapping saves

# Save the final state of the DataFrame
save_to_csv()
