# utils.py
import os
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Base data directory
DATA_DIR        = os.path.join(os.path.dirname(__file__), '..')
USERS_FILE      = os.path.join(DATA_DIR, 'users.json')
RIDES_DIR       = os.path.join(DATA_DIR, 'rides')
RIDES_FILE      = os.path.join(RIDES_DIR, 'rides.json')
COMPLAINTS_FILE = os.path.join(RIDES_DIR, 'complaints.json')
CARS_FILE       = os.path.join(RIDES_DIR, 'cars.json')

CATEGORIES = ['standard', 'medium', 'vip']
RATES      = {'standard': 1.5, 'medium': 2.0, 'vip': 3.5}

# Initialize geolocator
geolocator = Nominatim(user_agent="taxi_booking_app")

def ensure_dirs():
    os.makedirs(RIDES_DIR, exist_ok=True)
    for path, default in [
        (USERS_FILE, []),
        (RIDES_FILE, []),
        (COMPLAINTS_FILE, []),
        (CARS_FILE, [])
    ]:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=2)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# — Users API —
def load_users():
    return load_json(USERS_FILE)

def load_user(username):
    for u in load_users():
        if u['username'] == username:
            return u
    return None

def save_user(user):
    users = load_users()
    for i, u in enumerate(users):
        if u['username'] == user['username']:
            users[i] = user
            break
    else:
        users.append(user)
    save_json(USERS_FILE, users)

# — Geocoding & Distance —
def get_coordinates(address):
    loc = geolocator.geocode(address, country_codes='SA')
    return (loc.latitude, loc.longitude) if loc else None

def calculate_distance(orig, dest):
    o = get_coordinates(orig)
    d = get_coordinates(dest)
    return geodesic(o, d).km if o and d else None

def estimate_time(distance, speed_kmh=60):
    return (distance / speed_kmh) * 60
