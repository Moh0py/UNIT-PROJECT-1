import os
import json
from utils import ensure_data_dirs, RIDES_DIR, print_car
from auth import register, login, show_user_dashboard
from booking import book_ride
from simulation import simulate_arrival
from billing import print_receipt
from rating import rate_ride
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeocoder")

def main():
    ensure_data_dirs()

    while True:
        print_car()
        choice = show_main_menu()
        
        if choice == "1":
            print_car()
            register()
        elif choice == "2":
            print_car()
            user = login()
            if user:
                handle_logged_in_user(user)
        elif choice == "3":
            print_car()
            print("Goodbye!")
            break
        else:
            print_car()
            print("Invalid choice. Please choose 1, 2 or 3.")

def show_main_menu():
    print("Welcome to Taxi Booking System")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    return input("Choose an option: ").strip()

def handle_logged_in_user(user):
    while True:
        print_car()
        show_user_dashboard(user)
        sub_choice = show_user_menu()

        if sub_choice == "1":
            book_and_process_ride(user)
        elif sub_choice == "2":
            view_rides(user)
        elif sub_choice == "3":
            print_car()
            print("Logging out...\n")
            break
        else:
            print_car()
            print("Invalid choice. Please try again.")

def show_user_menu():
    print("1) Book a ride")
    print("2) View my rides")
    print("3) Logout")
    return input("Choose an option: ").strip()

def book_and_process_ride(user):
    print_car()
    ride_file = book_ride(user)
    path = os.path.join(RIDES_DIR, ride_file)
    with open(path) as f:
        ride = json.load(f)

    print_car()
    simulate_arrival(ride["distance"])
    print_receipt(user, ride)
    rate_ride(ride_file)

def view_rides(user):
    print_car()
    if not user.get("rides"):
        print("No rides yet.")
    else:
        print("\nYour Rides:")
        for fn in user["rides"]:
            print("-", fn)

if __name__ == "__main__":
    main()
