import os
import json
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic  # استيراد دالة لحساب المسافة
from utils import RIDES_DIR, save_user

geolocator = Nominatim(user_agent="myGeocoder")

def book_ride(user: dict) -> str:
    origin = input("Pickup location: ").strip()
    destination = input("Destination: ").strip()
    
    origin_location = geolocator.geocode(origin)
    destination_location = geolocator.geocode(destination)
    
    if not origin_location or not destination_location:
        return "Error: One of the locations could not be found."

    origin_lat = origin_location.latitude
    origin_lon = origin_location.longitude
    destination_lat = destination_location.latitude
    destination_lon = destination_location.longitude
    
    # حساب المسافة بين نقطتي البداية والوجهة
    origin_coords = (origin_lat, origin_lon)
    destination_coords = (destination_lat, destination_lon)
    distance = geodesic(origin_coords, destination_coords).km  # المسافة بالكيلومترات
    
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    
    ride = {
        "user": user['username'],
        "origin": origin,
        "destination": destination,
        "origin_coordinates": {"latitude": origin_lat, "longitude": origin_lon},
        "destination_coordinates": {"latitude": destination_lat, "longitude": destination_lon},
        "distance": distance,  # إضافة المسافة
        "timestamp": ts,
        "status": "booked"
    }
    
    filename = f"{user['username']}_{ts}.json"
    path = os.path.join(RIDES_DIR, filename)
    
    with open(path, 'w') as f:
        json.dump(ride, f, indent=2)
    
    user.setdefault('rides', []).append(filename)
    save_user(user)
    
    return filename
