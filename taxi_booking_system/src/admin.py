# admin.py
from utils import load_json, load_users, RIDES_FILE, COMPLAINTS_FILE, CARS_FILE, save_json
from auth import edit_profile
from colorama import Fore

def view_drivers():
    users = load_users()
    rides = load_json(RIDES_FILE)
    cars  = load_json(CARS_FILE)

    
    for user in users:
        if user.get('role') == 'driver':
            
            user_cars = [car for car in cars if car.get('driver') == user['username']]
            plate = user_cars[0]['plate'] if user_cars else "N/A"


            driver_rides = [r for r in rides if r.get('driver') == user['username']]
            ratings = [r['rating'] for r in driver_rides if r.get('rating') is not None]
            avg = (sum(ratings) / len(ratings)) if ratings else 0

            print(f"🚖 Driver: {user['username']} | Plate: {plate} | Rating: {avg:.2f}")

def view_cars():
    cars = load_json(CARS_FILE)
    for c in cars:
        print(  f"🚗 ID: {c['id']} | Plate: {c['plate']} | Category: {c['category']} | Status: {c['status']}")

def view_complaints():
    complaints = load_json(COMPLAINTS_FILE)
    for c in complaints:
        print(f" {c['id']} from {c['from_user']} about {c['about_driver']}: {c['message']} (Status: {c['status']})")

def edit_car_status():
    cars = load_json(CARS_FILE)
    for i, car in enumerate(cars, 1):
        print(f"{i}. ID: {car['id']} | Plate: {car['plate']} | Status: {car['status']}")
    idx = input("Select car number to update: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(cars)):
        print(" Invalid selection.")
        return
    car = cars[int(idx)-1]
    new_status = input("New status (ready/busy): ").strip().lower()
    if new_status not in ['ready', 'busy']:
        print(" Invalid status.")
        return
    car['status'] = new_status
    save_json(CARS_FILE, cars)
    print(" Car status updated.")

def admin_menu(admin_user):
    print(f"👮 Admin: {admin_user['username']}")
    while True:
        print(Fore.YELLOW + "\n--- Admin Menu ---")
        print()
        print("1. View Drivers")
        print("2. View Cars")
        print("3. View Complaints")
        print("4. Edit Car Status")
        print("5. Edit Profile")
        print("6. Logout")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            view_drivers()
        elif choice == '2':
            view_cars()
        elif choice == '3':
            view_complaints()
        elif choice == '4':
            edit_car_status()
        elif choice == '5':
            edit_profile(admin_user)
        elif choice == '6':
            print(" Logged out.")
            break
        else:
            print(" Invalid option.")
