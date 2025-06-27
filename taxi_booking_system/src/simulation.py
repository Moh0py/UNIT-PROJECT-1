import time, sys

def simulate_arrival(distance: int):
    print("\nSimulating taxi arrival...")
    progress = 0
    while progress < distance:
        sys.stdout.write(f"🚖{'-'*progress}📍\r")
        sys.stdout.flush()
        time.sleep(1)
        progress += 1
    print("✅ Taxi has arrived!\n")
