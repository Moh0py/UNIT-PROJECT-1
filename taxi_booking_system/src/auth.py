from utils import load_user, save_user

def create_admin_account():
    """Ensure an admin user exists."""
    if not load_user("admin"):
        admin = {
            'username': "admin",
            'password': "admin",
            'name': "Admin User",
            'email': "admin@example.com",
            'phone': "0000000000",
            'role': "admin",
            'rides': [],
            'complaints': [],
            'category': None
        }
        save_user(admin)
        print("✅ Admin account created.")
       

def register_user():
    """Interactively register a new standard user."""
    while True:
        username = input("Choose username: ")
        if load_user(username):
            print("⚠️ Username already exists.")
            
            continue
        break
    while True:    
        email = input("Email (@gmail.com): ")
        if not email.endswith("@gmail.com"):
            print("⚠️ Only Gmail addresses are allowed.")
            continue
        break

    while True:
        phone = input("Phone (10 digits): ")
        if not (phone.isdigit() and len(phone) == 10):
            print("⚠️ Phone number must be exactly 10 digits.")
            continue
        
        name = input("Full name: ")
        password = input("Password: ")

        user = {
            'username': username,
            'email': email,
            'phone': phone,
            'name': name,
            'password': password,
            'role': 'user',
            'rides': [],
            'complaints': [],
            'category': 'standard'
        }
        save_user(user)
        print("✅ Registration successful.")
        break

def login_user():
    """Interactively authenticate a user and return their data."""
    username = input("Username: ")
    password = input("Password: ")
    user = load_user(username)
    if not user or user['password'] != password:
        print("❌ Invalid credentials.")
        return None
    print(f"👋 Welcome, {user['name']}!")
    return user

def edit_profile(user):
    """Allow the logged-in user to update their own profile."""
    if not user:
        print("❌ No user provided.")
        return

    print("\n--- Edit Profile ---")
    new_username = input(f"New username (current: {user['username']}) or Enter to skip: ")
    new_email    = input(f"New email (current: {user['email']}) or Enter to skip: ")
    new_phone    = input(f"New phone (current: {user['phone']}) or Enter to skip: ")
    new_name     = input(f"New full name (current: {user['name']}) or Enter to skip: ")
    new_password = input("New password or Enter to skip: ")

    if new_username:
     user['username'] = new_username

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