from utils import load_json, load_users, RIDES_FILE, COMPLAINTS_FILE, CARS_FILE, save_json
from colorama import Fore
def view_drivers():
    rides = load_json(RIDES_FILE)
    for user in load_users():
        if user.get('role') == 'driver':
            trips   = [r for r in rides if r.get('driver') == user['username']]
            ratings = [r['rating'] for r in trips if r.get('rating') is not None]
            avg     = (sum(ratings) / len(ratings)) if ratings else 0
            print(f"🚖 {user['username']}: {len(trips)} trips, ⭐ {avg:.2f}")


def view_cars():
    cars = load_json(CARS_FILE)
    
    for c in cars:
        print(Fore.Red,f"🚗 ID: {c['id']} | Plate: {c['plate']} | {c['category']} | {c['status']}")


def view_complaints():
    complaints = load_json(COMPLAINTS_FILE)
    for c in complaints:
        print(f"⚠️ {c['id']} from {c['from_user']} about {c['about_driver']}: {c['message']} (Status: {c['status']})")


def edit_car_status():
    cars = load_json(CARS_FILE)
    for car in cars:
        print(f"{car['id']} | Plate: {car['plate']} | Status: {car['status']}")
    car_id = input("Enter Car ID to edit: ")
    for car in cars:
        if car['id'] == car_id:
            new_status = input("Enter new status (ready/busy): ")
            car['status'] = new_status
            save_json(CARS_FILE, cars)
            print(f"✅ Car {car_id} status updated to {new_status}")
            return
    print("❌ Car not found.")


def admin_menu(user):
    while True:
        print(f"\n=== Admin Menu (Logged in as {user['username']}) ===")
        print("1) View Drivers")
        print("2) View Cars")
        print("3) View Complaints")
        print("4) Edit Car Status")
        print("5) Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            view_drivers()
        elif choice == '2':
            view_cars()
        elif choice == '3':
            view_complaints()
        elif choice == '4':
            edit_car_status()
        elif choice == '5':
            print("🔒 Logging out of admin.")
            break
        else:
            print("❌ Invalid option.")
