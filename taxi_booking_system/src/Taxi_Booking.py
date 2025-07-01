import colorama
from colorama import Fore, Style
from utils import ensure_data_files
from auth import register_user, login_user, find_user, save_user
from booking import select_category, estimate_ride, book_ride, view_rides
from rating import rate_ride
from complaint import file_complaint
from admin import admin_menu

colorama.init(autoreset=True)

def print_box(title, opts, clr):
    w=max(len(title),*(len(o) for o in opts))+4
    print(clr+"╔"+"═"*w+"╗")
    print(clr+f"║ {title.center(w-2)} ║")
    print(clr+"╠"+"═"*w+"╣")
    for o in opts: print(clr+f"║ {o.ljust(w-2)} ║")
    print(clr+"╚"+"═"*w+"╝"+Style.RESET_ALL)


def user_menu(user):
    opts=["1.select category","2.estimate","3.book","4.view rides","5.rate","6.complaint","7.edit","8.logout"]
    while True:
        print_box("User Menu",opts,Fore.YELLOW)
        c=input(Fore.CYAN+"Choice:"+Style.RESET_ALL).strip()
        if c=='1': select_category(user)
        elif c=='2': estimate_ride(user)
        elif c=='3': book_ride(user)
        elif c=='4': view_rides(user)
        elif c=='5': rate_ride(user)
        elif c=='6': file_complaint(user)
        elif c=='7': from auth import edit_profile; edit_profile(user)
        elif c=='8': break


def main():
    ensure_data_files()
    if not find_user('admin'):
        save_user({'username':'admin','password':'admin','role':'admin','category':None,'rides':[],'complaints':[]})
    opts=["1.register","2.login","3.admin login","4.exit"]
    while True:
        print_box("Taxi Booking System",opts,Fore.CYAN)
        c=input(Fore.CYAN+"Choice:"+Style.RESET_ALL).strip()
        if c=='1': user_menu(register_user())
        elif c=='2': u=login_user(); user_menu(u) if u and u['role']!='admin' else print("Denied")
        elif c=='3': u=login_user(); admin_menu() if u and u['role']=='admin' else print("Denied")
        elif c=='4': print("Goodbye"); break

if __name__=='__main__':
    main()