from booking import view_rides
from utils import load_json, save_json, COMPLAINTS_FILE
from datetime import datetime

def file_complaint(user):
    
    try:  
     view_rides(user)
     if not user['rides']:
            print("No rides to file a complaint against.")
            return
    except Exception as e:
        print(f"Error viewing rides: {e}")
        return
    finally:
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
    if not message:
        print("Complaint message cannot be empty Plz try again.")
        return

    complaints = load_json(COMPLAINTS_FILE)
    complaints.append(comp)
    save_json(COMPLAINTS_FILE, complaints)
    print(f"✅ Complaint {comp_id} submitted.")
