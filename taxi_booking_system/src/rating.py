import os
import json
from utils import RIDES_DIR

def rate_ride(filename: str):
    path = os.path.join(RIDES_DIR, filename)
    with open(path) as f:
        ride = json.load(f)
    while True:
        rating = input("Enter rating (1-5): ").strip()
        if rating in ('1','2','3','4','5'):
            print("Thank you for your rating.")
            ride['rating'] = int(rating)
            break
    with open(path, 'w') as f:
        json.dump(ride, f, indent=2)
    print(f"Rating {rating} saved for ride {filename}")