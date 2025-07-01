import time, sys

def simulate_arrival(distance, driver=None):
    print(f"{'Driver '+driver+' en route' if driver else 'Taxi en route'}")
    for i in range(int(distance)):
        sys.stdout.write("-"*i+"\r"); sys.stdout.flush(); time.sleep(0.5)
    print(f"{'Driver '+driver+' arrived' if driver else 'Taxi arrived'}")