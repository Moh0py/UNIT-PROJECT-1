from utils import load_json, save_json, USERS_FILE, DRIVERS_FILE


def load_passengers(): return load_json(USERS_FILE)

def load_drivers():   return load_json(DRIVERS_FILE)

def find_user(username):
    """Search passengers+drivers."""
    for u in load_passengers() + load_drivers():
        if u['username'] == username:
            return u
    return None


def save_user(user):
    """Save to passengers.json or drivers.json."""
    target = DRIVERS_FILE if user['role']=='driver' else USERS_FILE
    users = load_json(target)
    for i,u in enumerate(users):
        if u['username']==user['username']:
            users[i]=user; break
    else:
        users.append(user)
    save_json(target, users)


def register_user():
    print("Register new account:")
    while True:
        uname=input("Username: ").strip()
        if find_user(uname): print("Already exists.")
        else: break
    pwd=input("Password: ").strip()
    role=input("Role (passenger/driver): ").strip().lower()
    if role not in ('passenger','driver'): role='passenger'
    user={'username':uname,'password':pwd,'role':role,'category':None,'rides':[],'complaints':[]}
    save_user(user); print("Registration successful.")
    return user


def login_user():
    print("Login:")
    uname=input("Username: ").strip()
    pwd=input("Password: ").strip()
    user=find_user(uname)
    if user and user['password']==pwd:
        print(f"Welcome, {uname}!"); return user
    print("Invalid credentials.")
    return None


def edit_profile(user):
    print("Edit Profile:")
    new=input("New password (Enter to skip): ").strip()
    if new:
        user['password']=new; save_user(user); print("Password updated.")
    else: print("No changes made.")
    new=input("New username (Enter to skip): ").strip()
    if new:
        user['username']=new; save_user(user); print("Username updated.")
    else: print("No changes made.")
