import os
import json
from datetime import datetime
from utils import RIDES_DIR, save_user

def book_ride(user: dict) -> str:
    origin = input("Pickup location: ").strip()
    destination = input("Destination: ").strip()
    while True:
        dist = input("Enter distance in km: ").strip()
        if not dist.isdigit():
            continue
        distance = int(dist)
        break
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    ride = {
        "user": user['username'],
        "origin": origin,
        "destination": destination,
        "distance": distance,
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
