# taxi_booking_system/src/booking.py
import random
import time
from datetime import datetime
from utils import calculate_distance, estimate_time, load_json, save_json, RIDES_FILE
from auth import save_user, load_drivers

PAYMENT_METHODS = ['cash', 'visa', 'mada']
CATEGORIES = ['standard', 'medium', 'vip']
RATES = {'standard': 1.5, 'medium': 2.0, 'vip': 3.5}


def select_category(user):
    """Prompt user to select a taxi category."""
    print("Select category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    idx = int(input("Choice: ")) - 1
    user['category'] = CATEGORIES[idx] if 0 <= idx < len(CATEGORIES) else CATEGORIES[0]
    save_user(user)
    print(f"Category set to {user['category']}")


def estimate_ride(user):
    """Estimate distance, time, and fare for a potential ride."""
    if not user.get('category'):
        print("Select category first.")
        return
    origin = input("Pickup: ")
    destination = input("Destination: ")
    dist = calculate_distance(origin, destination)
    if dist is None:
        print("Could not calculate distance.")
        return
    duration = estimate_time(dist)
    fare = dist * RATES[user['category']]
    print(f"Distance: {dist} km | Time: {duration} min | Fare: {fare:.2f} SAR")


def simulate_arrival(distance, driver_name):
    """Visual simulation of taxi arrival with an ASCII progress bar."""
    print(f"Driver {driver_name} en route...")
    total = max(int(distance), 1)
    for i in range(total + 1):
        bar = '-' * i + '>' + ' ' * (total - i)
        print(f"[{bar}] {i}/{total} km", end='\r')
        time.sleep(1)
    print(f"\n🚕 Driver {driver_name} arrived.")


def book_ride(user):
    """Book a ride, assign driver, select payment, save record, and return ride details."""
    if not user.get('category'):
        print("Select category first.")
        return None

    origin = input("Pickup: ")
    destination = input("Destination: ")
    dist = calculate_distance(origin, destination)
    if dist is None:
        print("Could not calculate distance.")
        return None

    drivers = load_drivers()
    if not drivers:
        print("No drivers available.")
        return None
    driver = random.choice(drivers)['username']

    fare = dist * RATES[user['category']]
    ride_id = f"ride_{datetime.now():%Y%m%d%H%M%S}"

    print("Payment methods: ", ", ".join(PAYMENT_METHODS))
    pm = input("Choose payment method: ").strip().lower()
    if pm not in PAYMENT_METHODS:
        print("Invalid method, defaulting to cash.")
        pm = 'cash'

    ride_record = {
        'id': ride_id,
        'user': user['username'],
        'driver': driver,
        'origin': origin,
        'destination': destination,
        'category': user['category'],
        'distance': dist,
        'fare': fare,
        'payment_method': pm,
        'status': 'booked',
        'rating': None,
        'timestamp': datetime.now().isoformat()
    }

    rides = load_json(RIDES_FILE)
    rides.append(ride_record)
    save_json(RIDES_FILE, rides)

    if 'rides' not in user or not isinstance(user['rides'], list):
        user['rides'] = []
    user['rides'].append(ride_id)
    save_user(user)

    print(f"Booked {ride_id} with driver {driver}. Fare: {fare:.2f} SAR")
    return ride_record


def view_rides(user):
    """Display all rides for the current user."""
    rides = load_json(RIDES_FILE)
    my_rides = [r for r in rides if r.get('user') == user['username']]
    if not my_rides:
        print("No rides.")
        return
    for r in my_rides:
        print(
            f"{r['id']}: {r['origin']} → {r['destination']} | Driver: {r.get('driver', 'Unknown')} | Fare: {r['fare']:.2f} SAR | Paid by: {r.get('payment_method', 'N/A')}"
        )
