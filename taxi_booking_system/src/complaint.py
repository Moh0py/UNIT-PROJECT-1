from booking import view_rides
from utils import load_json, save_json, COMPLAINTS_FILE
from datetime import datetime

def file_complaint(user):
    """Submit a complaint linked to one of the user’s rides."""
    view_rides(user)
    ride_id = input("Ride ID for complaint: ").strip()
    message = input("Complaint message: ").strip()
    comp_id = f"comp_{datetime.now():%Y%m%d%H%M%S}"
    comp = {
        'id':      comp_id,
        'ride':    ride_id,
        'from':    user['username'],
        'message': message,
        'status':  'new'
    }

    complaints = load_json(COMPLAINTS_FILE)
    complaints.append(comp)
    save_json(COMPLAINTS_FILE, complaints)
    print(f"✅ Complaint {comp_id} submitted.")
