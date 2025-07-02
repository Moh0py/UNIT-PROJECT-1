import colorama
from colorama import Fore, Style
from utils import load_json, save_json, CARS_FILE, RIDES_FILE, COMPLAINTS_FILE


colorama.init(autoreset=True)

def print_box(title, opts, clr):
    padding_top_bottom = 1
    padding_left_right = 4

    
    content_width = max(
        len(title),
        *(len(o) for o in opts)
    ) + padding_left_right * 2

    
    print(clr + "╔" + "═" * content_width + "╗")

    
    for _ in range(padding_top_bottom):
        print(clr + "║" + " " * content_width + "║")

    
    title_line = title.center(content_width)
    print(clr + f"║{title_line}║")

    
    for _ in range(padding_top_bottom):
        print(clr + "║" + " " * content_width + "║")

    print(clr + "╠" + "═" * content_width + "╣")

    
    for o in opts:
        line = o.center(content_width)
        print(clr + f"║{line}║")

    print(clr + "╚" + "═" * content_width + "╝" + Style.RESET_ALL)

def view_drivers():
    
    rides = load_json(RIDES_FILE)
    scores = {}
    for r in rides:
        if r.get('rating') is not None:
            driver = r.get('driver', 'Unknown')
            scores.setdefault(driver, []).append(r['rating'])
    averages = [(d, sum(v)/len(v)) for d, v in scores.items()]
    averages.sort(key=lambda x: x[1], reverse=True)
    if not averages:
        print("No driver ratings yet.\n")
        return
    
    print("\nDrivers by average rating:")
    for d, avg in averages:
        print(f"  {d}: {avg:.2f}")
    print()


def view_cars():
    
    cars = load_json(CARS_FILE)
    if not cars:
        print("No cars available.\n")
        return
    
    print("\nCars:")
    for c in cars:
        cid    = c.get('id', 'N/A')
        driver = c.get('driver', 'N/A')
        plate  = c.get('plate', 'N/A')
        cat    = c.get('category', 'N/A')
        status = c.get('status', 'N/A')
        print(f"  {cid} | {driver} | {plate} | {cat} | {status}")
    print()


def view_complaints():

    comps = load_json(COMPLAINTS_FILE)
    if not comps:
        print("No complaints.\n")
        return
    
    print("\nComplaints:")
    for c in comps:
        cid     = c.get('id', 'N/A')
        ride    = c.get('ride', 'N/A')
        sender  = c.get('from', 'N/A')
        msg     = c.get('message', '')
        status  = c.get('status', 'N/A')
        print(f"  {cid}: from {sender} on {ride} — “{msg}” ({status})")
    print()


def edit_car_status():
    
    cars = load_json(CARS_FILE)
    if not cars:
        print("No cars available.\n")
        return
    
    print("\nSelect a car to update:")
    for idx, c in enumerate(cars, 1):
        print(f"  {idx}. {c.get('plate', 'N/A')} (status: {c.get('status', 'N/A')})")
    sel = input("Car number: ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(cars)):
        print("Invalid selection.\n")
        return
    new_status = input("New status (ready/busy or etc.): ").strip().lower()
    cars[int(sel)-1]['status'] = new_status
    save_json(CARS_FILE, cars)
    print("Car status updated.\n")


def delete_ride():
    
    rides = load_json(RIDES_FILE)
    if not rides:
        print("No rides to delete.\n")
        return
    print("\nSelect a ride to delete:")
    for idx, r in enumerate(rides, 1):
        print(f"  {idx}. {r.get('id', 'N/A')} — {r.get('user', 'N/A')} → {r.get('destination', 'N/A')}")
    sel = input("Ride number: ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(rides)):
        print("Invalid selection.\n")
        return
    removed = rides.pop(int(sel)-1)
    save_json(RIDES_FILE, rides)
    print(f"Removed ride {removed.get('id', 'N/A')}.\n")


def admin_menu():
    
    options = [
        "1. View drivers",
        "2. View cars",
        "3. View complaints",
        "4. Edit car status",
        "5. Delete ride",
        "6. Logout"
    ]
    while True:
        print_box("Taxi Rental Admin", options, Fore.MAGENTA)
        choice = input(Fore.CYAN + "Choice: " + Style.RESET_ALL).strip()
        if   choice == '1': view_drivers()
        elif choice == '2': view_cars()
        elif choice == '3': view_complaints()
        elif choice == '4': edit_car_status()
        elif choice == '5': delete_ride()
        elif choice == '6': break
        else: print("Invalid choice.\n")
