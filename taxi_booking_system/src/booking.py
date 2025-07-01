import random
import time
from datetime import datetime
from utils import calculate_distance, estimate_time, load_json, save_json, RIDES_FILE
from auth import save_user, load_drivers


PAYMENT_METHODS = ['cash', 'visa', 'mada']
CATEGORIES      = ['standard', 'medium', 'vip']
RATES           = {'standard': 1.5, 'medium': 2.0, 'vip': 3.5}


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
    dest   = input("Destination: ")
    dist   = calculate_distance(origin, dest)
    if dist is None:
        return
    duration = estimate_time(dist)
    fare     = dist * RATES[user['category']]
    print(f"Distance {dist} km | Time {duration} min | Fare {fare:.2f} SAR")


def simulate_arrival(distance, driver_name):
    """Visual simulation of taxi arrival by driver."""
    print(f"Driver {driver_name} en route.")
    for i in range(int(distance)):
        print("-" * i, end="\r")
        time.sleep(0.5)
    print(f"Driver {driver_name} arrived.")


def book_ride(user):
    """Book a ride, choose driver, select payment, and save the record."""
    if not user.get('category'):
        print("Select category first.")
        return

    # Gather ride details
    origin = input("Pickup: ")
    dest   = input("Destination: ")
    dist   = calculate_distance(origin, dest)
    if dist is None:
        return

    # Assign a random driver
    drivers = load_drivers()
    if not drivers:
        print("No drivers available.")
        return
    driver = random.choice(drivers)['username']

    # Calculate fare and ride ID
    fare    = dist * RATES[user['category']]
    ride_id = f"ride_{datetime.now():%Y%m%d%H%M%S}"

    # Choose payment method
    print("Payment methods:", ", ".join(PAYMENT_METHODS))
    pm = input("Choose payment method: ").strip().lower()
    if pm not in PAYMENT_METHODS:
        print("Invalid method, defaulting to cash.")
        pm = 'cash'

    # Prepare ride record
    ride_record = {
        'id':              ride_id,
        'user':            user['username'],
        'driver':          driver,
        'origin':          origin,
        'destination':     dest,
        'category':        user['category'],
        'distance':        dist,
        'fare':            fare,
        'payment_method':  pm,
        'status':          'booked',
        'rating':          None,
        'timestamp':       datetime.now().isoformat()
    }

    # Save ride
    rides = load_json(RIDES_FILE)
    rides.append(ride_record)
    save_json(RIDES_FILE, rides)

    # Update user's ride history
    user['rides'].append(ride_id)
    save_user(user)

    # Confirmation and simulation
    print(f"Booked {ride_id} with driver {driver}. Fare: {fare:.2f} SAR")
    simulate_arrival(dist, driver)


def view_rides(user):
    """Display all rides for the current user."""
    rides = load_json(RIDES_FILE)
    my_rides = [r for r in rides if r['user'] == user['username']]
    if not my_rides:
        print("No rides.")
        return
    for r in my_rides:
        driver = r.get('driver', 'Unknown')
        pm     = r.get('payment_method', 'N/A')
        print(
            f"{r['id']}: {r['origin']}→{r['destination']} "
            f"by {driver} | {r['fare']:.2f} SAR | paid with {pm}"
        )
