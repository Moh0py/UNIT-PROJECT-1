import json
import os
from .utils import USERS_DIR, get_user_path, save_user

def register():
    print("\n=== Register ===")
    
    while True:
        username = input("Enter new username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            continue
        if os.path.exists(get_user_path(username)):
            print("❌ Username already exists.")
            continue
        break

    
    while True:
        password = input("Enter password: ").strip()
        if not password:
            print("❌ Password cannot be empty.")
            continue
        break

 
    while True:
        phone = input("Enter phone (10 digits): ").strip()
        if not (phone.isdigit() and len(phone) == 10):
            print("❌ Phone must be exactly 10 digits.")
            continue
        break

  
    while True:
        email = input("Enter email: ").strip()
        if not email:
            print("❌ Email cannot be empty.")
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
    print("✅ Account created successfully!")
