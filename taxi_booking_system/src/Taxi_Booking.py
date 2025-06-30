# Taxi_Booking.py
import os
from utils import ensure_dirs, load_json, save_json, COMPLAINTS_FILE, RIDES_FILE
import auth, booking, rating, admin
from datetime import datetime
from auth import create_admin_account
from colorama import Fore
from geopy.geocoders import Nominatim

def handle_complaint(user):
    driver  = input("Driver username: ").strip()
    message = input("Complaint message: ").strip()
    complaints = load_json(COMPLAINTS_FILE)
    cid = f"complaint_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    complaints.append({
        'id': cid,
        'from_user': user['username'],
        'about_driver': driver,
        'message': message,
        'status': 'new'
    })
    save_json(COMPLAINTS_FILE, complaints)
    print(f"✅ Complaint {cid} submitted.")

def select_taxi_category(user):
    print("🚗 Categories:")
    print("1. standard\n2. medium\n3. vip")
    choice = input("Enter number: ").strip()
    cat_map = {'1': 'standard', '2': 'medium', '3': 'vip'}
    user['category'] = cat_map.get(choice, 'standard')
    from utils import save_user
    save_user(user)
    print(f"✅ Category set to {user['category']}.")

def view_rides(user):
    rides = load_json(RIDES_FILE)
    user_rides = [r for r in rides if r['user'] == user['username']]
    if not user_rides:
        print("🚘 No rides.")
        return
    for r in user_rides:
        print(f"{r['id']}: {r['origin']} → {r['destination']} | {r['fare']} SAR | {r['status']}")

def rate_rides(user):
    view_rides(user)
    ride_id = input("Ride ID to rate: ").strip()
    rating.rate_ride(ride_id)

def user_menu(user):
    print(f"\n👤 {user['username']} ({user['role']})")
    while True:
        print(Fore.YELLOW,"\n---- User Menu ----")
        print(Fore.WHITE,"1.Estimate ")
        print(Fore.WHITE,"2.Book ")
        print(Fore.WHITE,"3.Set Category ")
        print(Fore.WHITE,"4.My Rides")
        print(Fore.WHITE,"5.Rate Ride ")
        print(Fore.WHITE,"6.Complaint ")
        print(Fore.WHITE,"7.Edit Profile ")
        print(Fore.WHITE,"8.Logout")
        choice = input("Choice: ").strip()
        if choice == '1': booking.estimate_ride(user)
        elif choice == '2': booking.book_ride(user)
        elif choice == '3': select_taxi_category(user)
        elif choice == '4': view_rides(user)
        elif choice == '5': rate_rides(user)
        elif choice == '6': handle_complaint(user)
        elif choice == '7': auth.edit_profile(user)
        elif choice == '8':
            print("👋 Bye.")
            break
        else:
            print("❌ Invalid.")

def main():
    ensure_dirs()
    auth.create_admin_account()
    while True:
        print(Fore.YELLOW + "\n=== Taxi Booking ===")
        print()
        print(Fore.WHITE + "1.Register")
        print(Fore.WHITE + "2.Login")
        print(Fore.WHITE + "3.Admin Login")
        print(Fore.WHITE + "4.Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            u = auth.register_user()
            user_menu(u)
        elif choice == '2':
            u = auth.login_user()
            if u: user_menu(u)
        elif choice == '3':
            a = auth.login_user()
            if a and a.get('role')=='admin':
                admin.admin_menu(a)
            else:
                print("❌ Invalid admin.")
        elif choice == '4':
            print("👋 Exiting.")
            break
        else:
            print("❌ Invalid.")

if __name__ == "__main__":
    main()
