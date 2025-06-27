import os , json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_DIR = os.path.join(BASE_DIR, 'users.json')
RIDES_DIR = os.path.join(BASE_DIR, 'taxi.json')

def ensure_data_dirs():
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(RIDES_DIR, exist_ok=True)

def get_user_path(username:str)->str:
       return os.path.join(USERS_DIR, f"{username}.json")
    
def save_user(data:dict):
       with open(get_user_path(data['username']), 'w') as f:
           json.dump(data, f, indent=2)
    