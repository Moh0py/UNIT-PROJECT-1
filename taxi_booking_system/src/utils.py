import os
import json
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

# Data directory and file paths
DATA_DIR        = 'data'
USERS_FILE      = os.path.join(DATA_DIR, 'users.json')
DRIVERS_FILE    = os.path.join(DATA_DIR, 'drivers.json')
RIDES_FILE      = os.path.join(DATA_DIR, 'rides.json')
RATINGS_FILE    = os.path.join(DATA_DIR, 'ratings.json')
COMPLAINTS_FILE = os.path.join(DATA_DIR, 'complaints.json')
CARS_FILE       = os.path.join(DATA_DIR, 'cars.json')

# Initialize geocoder
geolocator = Nominatim(user_agent="taxi_booking_app")


def ensure_data_files():
    """Create data directory and JSON files if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in [USERS_FILE, DRIVERS_FILE, RIDES_FILE, RATINGS_FILE, COMPLAINTS_FILE, CARS_FILE]:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)


def load_json(path):
    """Load and return list from a JSON file. Returns [] if file is empty or invalid."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_json(path, data):
    """Save list to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def calculate_distance(origin, destination):
    """
    Calculate geodesic distance (km) using Haversine formula.
    Returns rounded float or None.
    """
    try:
        loc1 = geolocator.geocode(origin, timeout=10)
        loc2 = geolocator.geocode(destination, timeout=10)
        if not loc1 or not loc2:
            print(f"Error geocoding '{origin}' or '{destination}'")
            return None
        lat1, lon1 = radians(loc1.latitude), radians(loc1.longitude)
        lat2, lon2 = radians(loc2.latitude), radians(loc2.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return round(6371.0 * c, 2)
    except Exception as e:
        print(f"Distance error: {e}")
        return None


def estimate_time(distance_km, speed_kmh=60):
    """Estimate travel time in minutes given distance and speed."""
    if distance_km is None:
        return None
    return int(round((distance_km / speed_kmh) * 60))
