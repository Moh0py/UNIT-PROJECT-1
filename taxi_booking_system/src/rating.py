from utils import load_json, save_json, RIDES_FILE
def rate_ride(ride_id):
    rides = load_json(RIDES_FILE)
    if not rides:
        print("🚘 No rides available to rate.")
        return

    for ride in rides:
        if ride['id'] == ride_id:
            while True:
                score_str = input(f"Enter rating for {ride_id} (1-5): ").strip()
                #try:
                score = int(score_str)
                if 1 <= score <= 5:
                        ride['rating'] = score
                        save_json(RIDES_FILE, rides)
                        print(f"✅ Ride {ride_id} rated {score}.")
                        break
    #                 else:
    #                     raise ValueError
    #             except ValueError:
    #                 print("❌ Invalid score. Enter a number between 1 and 5.")
    #         return
    # print(f"❌ Ride {ride_id} not found.")