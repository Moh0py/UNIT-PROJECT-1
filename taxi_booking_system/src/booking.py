from utils import (
    calculate_distance,
    estimate_time,
    load_json,
    save_json,
    RIDES_FILE,
    RATES,
    CARS_FILE,
    save_user
)
from datetime import datetime
import time
import random
from geopy.geocoders import Nominatim

def estimate_ride(user):
    if not user.get('category') or user['category'] not in RATES:
        print("⚠️ Please select your taxi category first!")
        return
    origin = input("Pickup location: ")
    destination = input("Destination: ")
    distance = calculate_distance(origin, destination)
    if distance is None:
        print("❌ Could not calculate distance.")
        return

    duration_minutes = estimate_time(distance)
    rate = RATES[user['category']]
    fare = distance * rate
    print(f" 🛣️  Distance:          {distance:.2f} km")
    print(f" ⏱️ Estimated time:     {duration_minutes:.0f} minutes")
    print(f" 💰 Estimated fare:     {fare:.2f} SAR")
    print(f" 🚗 Category:          {user['category']}")

def book_ride(user):
    
    if not user.get('category') or user['category'] not in RATES:
        print("⚠️ Please select your taxi category first!")
        return

    
    origin = input("Pickup location: ")
    destination = input("Destination: ")
    distance = calculate_distance(origin, destination)
    if distance is None:
        print("❌ Could not calculate distance.")
        return

    
    duration_minutes = estimate_time(distance)
    duration_hours = duration_minutes / 60
    rate = RATES[user['category']]
    fare = distance * rate

    
    cars = load_json(CARS_FILE)
    available = [c for c in cars if c['category'] == user['category'] and c['status'] == 'ready']
    if not available:
        print("❌ No available cars in your category.")
        return

    
    car = random.choice(available)
    car['status'] = 'busy'
    save_json(CARS_FILE, cars)

    
    ride_id = f"ride_{datetime.now():%Y%m%d%H%M%S}"
    ride = {
        'id': ride_id,
        'user': user['username'],
        'origin': origin,
        'destination': destination,
        'category': user['category'],
        'distance_km': round(distance, 2),
        'duration_minutes': round(duration_minutes, 1),
        'duration_hours': round(duration_hours, 2),
        'fare': round(fare, 2),
        'driver': car['driver'],
        'car_plate': car['plate'],
        'timestamp': datetime.now().isoformat(),
        'status': 'booked',
        'rating': None
    }

    
    rides = load_json(RIDES_FILE)
    rides.append(ride)
    save_json(RIDES_FILE, rides)

   
    user.setdefault('rides', []).append(ride_id)
    save_user(user)

    
    print(f"✅ Ride {ride_id} booked!")
    print(f"🚖 Driver: {car['driver']} | Plate: {car['plate']}")
    print(f"🛣️ {ride['distance_km']} km | ⏱️ {ride['duration_hours']} hrs | 💰 {ride['fare']} SAR")

    
    for i in range(20):
        print(" " * i + "🚕", end="\r")
        time.sleep(0.1)
    print("🚕 Taxi has arrived!")

    
    for c in cars:
        if c['id'] == car['id']:
            c['status'] = 'ready'
            break
    save_json(CARS_FILE, cars)
