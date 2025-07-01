from booking import view_rides
from utils import load_json, save_json, RIDES_FILE

def rate_ride(user):
    
    view_rides(user)

    
    ride_id = input("Enter ride ID to rate: ").strip()
    if not ride_id:
        print("❌ No ride ID entered.")
        return

    
    rides = load_json(RIDES_FILE)
    
    for r in rides:
        if r['id'] == ride_id and r['user'] == user['username']:
            
            try:
                score = int(input("Enter rating (1-5): ").strip())
            except ValueError:
                print("❌ Invalid input; please enter a number.")
                return
            if score < 1 or score > 5:
                print("❌ Rating must be between 1 and 5.")
                return
            
            r['rating'] = score
            save_json(RIDES_FILE, rides)
            print("✅ Thank you for your rating!")
            return

    print("❌ Ride not found or not owned by you.")
