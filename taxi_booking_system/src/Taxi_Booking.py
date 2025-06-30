import os
from utils import ensure_dirs, load_json, save_json, COMPLAINTS_FILE
import auth, booking, rating, admin
from datetime import datetime
from auth import create_admin_account
from colorama import Fore

def handle_complaint(user):
    driver = input("Driver username: ")
    message = input("Complaint message: ")
    complaints = load_json(COMPLAINTS_FILE)
    cid = f"complaint_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    complaints.append({
        'id': cid,
        'from_user': user['username'],
        'about_driver': driver,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'status': 'open'
    })
    save_json(COMPLAINTS_FILE, complaints)
    print(f"✅ Complaint {cid} submitted.")

def select_taxi_category(user):
    print("\nSelect Taxi Category:")
    print()
    print("1) standard")
    print("2) medium")
    print("3) vip")
    while True:
        cat = input("Enter choice: ").strip()
        mapping = {'1':'standard','2':'medium','3':'vip'}
        if cat in mapping:
            user['category'] = mapping[cat]
            print(f"✅ Selected category: {user['category']}")
            break
        print("❌ Invalid choice; select 1, 2, or 3.")

def view_rides(user):
    if user.get('rides'):
        for r in user['rides']:
            print(f"- {r}")
    else:
        print("🚘 No rides found.")

def rate_rides(user):
    if user.get('rides'):
        for r in user['rides']:
            rating.rate_ride(r)
    else:
        print("🚘 No rides to rate.")

def user_menu(user):
    select_taxi_category(user)
    while True:
        print(f"\nLogged in as: {user['username']} ({user['category']})")
        print("=== User Menu ===")
        print()
        print(Fore.CYAN + "1) Estimate Ride")
        print(Fore.CYAN + "2) Book Ride")
        print(Fore.CYAN + "3) View My Rides")
        print(Fore.CYAN + "4) Rate a Ride")
        print(Fore.CYAN + "5) Complain about Driver")
        print(Fore.CYAN + "6) Edit Profile")
        print(Fore.CYAN + "7) Logout")
        cmd = input("Option: ").strip()

        if cmd == '1':
            booking.estimate_ride(user)
        elif cmd == '2':
            booking.book_ride(user)
        elif cmd == '3':
            view_rides(user)
        elif cmd == '4':
            rate_rides(user)
        elif cmd == '5':
            handle_complaint(user)
        elif cmd == '6':
            auth.edit_profile(user)
        elif cmd == '7':
            auth.save_user(user)
            break
        else:
            print("❌ Invalid option.")

def main():
    ensure_dirs()
    create_admin_account()

    while True:
        print(Fore.YELLOW + "\n=== Welcome to Taxi Booking System ===")
        print()
        print(Fore.WHITE +    "Please choose an option:")
        print()
        print(Fore.YELLOW + "1) Register")
        print(Fore.YELLOW + "2) Login")
        print(Fore.YELLOW + "3) Admin Login")
        print(Fore.YELLOW + "4) View Available Cars")
        print(Fore.YELLOW + "5) Quit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            auth.register_user()
        elif choice == '2':
            user = auth.login_user()
            if user:
                user_menu(user)
            else:
                input("Press Enter to continue...")
        elif choice == '3':
            admin_user = auth.login_user()
            if admin_user and admin_user.get('role')=='admin':
                admin.admin_menu(admin_user)
            else:
                print("❌ Invalid admin credentials.")
        elif choice == '4':
            admin.view_cars()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
