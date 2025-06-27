# auth.py
import os
import json
from utils import USERS_DIR, get_user_path, save_user, print_car

def register():
    print_car()
    while True:
        username = input("Enter new username: ").strip()
        if not username or os.path.exists(get_user_path(username)):
            continue
        break
    while True:
        password = input("Enter password: ").strip()
        if not password:
            continue
        break
    while True:
        phone = input("Enter phone (10 digits): ").strip()
        if not (phone.isdigit() and len(phone) == 10):
            continue
        break

    while True:

        email = input("Enter email: ").strip()
        if not email:
            continue
        break
    
    data = {
        "username": username,
        "password": password,
        "phone": phone,
        "email": email,
        "driver": False,
        "rides": []
    }
    save_user(data)

def login():
    print_car()
    if not os.listdir(USERS_DIR):
        return None
    while True:
        username = input("Enter your username: ").strip()
        path = get_user_path(username)
        if os.path.isfile(path):
            break
    with open(path) as f:
        user = json.load(f)
    while True:
        print_car()
        password = input("Enter your password: ").strip()
        if user.get("password") == password:
            break
    return user

def show_user_dashboard(user: dict):
    print_car()
    print(f"Username: {user['username']}")
    print(f"Phone:    {user['phone']}")
    print(f"Email:    {user['email']}")
    print(f"Driver:   {user.get('driver')}")
    print(f"Rides:    {len(user.get('rides', []))}\n")

def edit_profile(user: dict):
    print_car()
    while True:
        phone = input("Enter new phone (10 digits): ").strip()
        if not (phone.isdigit() and len(phone) == 10):
            continue
        break
    while True:
        print_car()
        email = input("Enter new email: ").strip()
        if not email:
            continue
        break
    user['phone'] = phone
    user['email'] = email
    save_user(user)
