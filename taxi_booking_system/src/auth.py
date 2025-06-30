
from utils import load_user, load_users, save_user

def create_admin_account():

    admin_user = load_user('admin')
    if not admin_user:
        default = {
            'username': 'admin',
            'password': 'admin',
            'name': 'Administrator',
            'email': 'admin@example.com',
            'phone': '',
            'role': 'admin',
            'rides': [],
            'complaints': [],
            'category': None
        }
        save_user(default)
        print("✅ Default admin account created (admin / admin123).")

def register_user():
    print("📝 Register")
    while True:
        username = input("Username: ").strip()
        if load_user(username):
            print("❌ Username already exists.")
        else:
            break
    password = input("Password: ").strip()
    name     = input("Full name: ").strip()
    email    = input("Email: ").strip()
    phone    = input("Phone: ").strip()
    role     = input("Role (passenger/driver): ").strip().lower()
    if role not in ['passenger', 'driver']:
        role = 'passenger'
    user = {
        'username': username,
        'password': password,
        'name': name,
        'email': email,
        'phone': phone,
        'role': role,
        'rides': [],
        'complaints': [],
        'category': None
    }
    save_user(user)
    print("✅ Registration successful.")
    return user

def login_user():
    print("🔑 Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = load_user(username)
    if user and user['password'] == password:
        print(f"✅ Welcome, {user['name']}!")
        return user
    print("❌ Invalid credentials.")
    return None

def edit_profile(user):
    print("✍️ Edit Profile")
    new_email    = input(f"New email (current: {user['email']}) or Enter to skip: ").strip()
    new_phone    = input(f"New phone (current: {user['phone']}) or Enter to skip: ").strip()
    new_name     = input(f"New full name (current: {user['name']}) or Enter to skip: ").strip()
    new_password = input("New password or Enter to skip: ").strip()
    if new_email:
        user['email'] = new_email
    if new_phone:
        user['phone'] = new_phone
    if new_name:
        user['name'] = new_name
    if new_password:
        user['password'] = new_password
    save_user(user)
    print("✅ Profile updated.")
