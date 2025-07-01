import os
import json
from typing import Optional, Union
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

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


def ensure_data_files() -> None:
    """Create data directory and JSON files if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in [
        USERS_FILE, DRIVERS_FILE, RIDES_FILE,
        RATINGS_FILE, COMPLAINTS_FILE, CARS_FILE
    ]:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)


def load_json(path: str) -> list:
    """Load and return list from a JSON file. Returns [] on error."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_json(path: str, data: list) -> None:
    """Save list to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def calculate_distance(origin: str, destination: str) -> Optional[float]:
    """
    Calculate geodesic distance (km) on the WGS-84 ellipsoid.
    Returns rounded float or None if geocoding fails.
    """
    try:
        loc1 = geolocator.geocode(origin, timeout=10)
        loc2 = geolocator.geocode(destination, timeout=10)
        if not loc1 or not loc2:
            print(f"Error geocoding '{origin}' or '{destination}'")
            return None

        return round(
            geodesic(
                (loc1.latitude, loc1.longitude),
                (loc2.latitude, loc2.longitude)
            ).km
            
        )
    except Exception as e:
        print(f"Distance error: {e}")
        return None


def estimate_time(
    distance_km: Union[float, int, None],
    speed_kmh: float = 60.0
) -> Optional[int]:

    if distance_km is None or speed_kmh <= 0:
        return None
    minutes = (distance_km / speed_kmh) * 60
    return int(round(minutes))


def format_travel_time(minutes: Optional[int]) -> str:
    
    if minutes is None:
        return "--"
    hours, mins = divmod(minutes, 60)
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if mins or not parts:
        parts.append(f"{mins}m")
    return " ".join(parts)
