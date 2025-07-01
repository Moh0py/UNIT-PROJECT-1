from utils import calculate_distance, estimate_time, RATES

def calculate_fare():
    o=input("Pickup:")
    d=input("Destination:")
    print("Rates:",RATES)
    cat=input("Category:")
    dist=calculate_distance(o,d)
    if dist is None: return
    t=estimate_time(dist); fare=dist*RATES.get(cat,0)
    print(f"{dist}km | {t}min | {fare:.2f}SAR")
