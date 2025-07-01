import colorama
from colorama import Fore, Style
from utils import ensure_data_files
from auth import register_user, login_user, find_user, save_user
from booking import select_category, estimate_ride, book_ride, view_rides
from rating import rate_ride
from complaint import file_complaint
from admin import admin_menu
from simulation import simulate_ascii_route  


colorama.init(autoreset=True)


def print_box(title, opts, clr):
    w = max(len(title), *(len(o) for o in opts)) + 4
    print(clr + "╔" + "═" * w + "╗")
    print(clr + f"║ {title.center(w-2)} ║")
    print(clr + "╠" + "═" * w + "╣")
    for o in opts:
        print(clr + f"║ {o.ljust(w-2)} ║")
    print(clr + "╚" + "═" * w + "╝" + Style.RESET_ALL)


def user_menu(user):
    opts = [
        "1. Select category",
        "2. Estimate ride",
        "3. Book a ride",
        "4. View my rides",
        "5. Rate a ride",
        "6. File a complaint",
        "7. Edit profile",
        "8. Logout"
    ]
    while True:
        print_box("User Menu", opts, Fore.YELLOW)
        choice = input(Fore.CYAN + "Choice: " + Style.RESET_ALL).strip()

        if choice == '1':
            select_category(user)
        elif choice == '2':
            estimate_ride(user)
        elif choice == '3':
            record = book_ride(user)  
            if record:
                simulate_ascii_route([record['origin'], record['destination']])
        elif choice == '4':
            view_rides(user)
        elif choice == '5':
            rate_ride(user)
        elif choice == '6':
            file_complaint(user)
        elif choice == '7':
            from auth import edit_profile
            edit_profile(user)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

        
def main():
    ensure_data_files()
    # Ensure admin user exists
    if not find_user('admin'):
        save_user({
            'username': 'admin',
            'password': 'admin',
            'role': 'admin',
            'category': None,
            'rides': [],
            'complaints': []
        })

    opts = ["1. Register", "2. Login", "3. Admin login", "4. Exit"]
    while True:
        print_box("Taxi Booking System", opts, Fore.CYAN)
        choice = input(Fore.CYAN + "Choice: " + Style.RESET_ALL).strip()
        if choice == '1':
            user = register_user()
            if user:
                user_menu(user)
        elif choice == '2':
            user = login_user()
            if user and user['role'] != 'admin':
                user_menu(user)
            else:
                print("Access denied.")
        elif choice == '3':
            admin = login_user()
            if admin and admin['role'] == 'admin':
                admin_menu()
            else:
                print("Access denied.")
        elif choice == '4':
            print("Thank you for using the Taxi Booking System!")
            break


if __name__ == '__main__':
    main()