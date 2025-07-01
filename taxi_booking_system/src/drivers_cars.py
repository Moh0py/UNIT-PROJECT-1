import json

def merge_cars_into_drivers():
    drivers_file = 'data/drivers.json'
    cars_file = 'data/cars.json'

    # Load drivers
    with open(drivers_file, 'r', encoding='utf-8') as f:
        drivers = json.load(f)

    # Load cars
    with open(cars_file, 'r', encoding='utf-8') as f:
        cars = json.load(f)

    # Build a dictionary of cars by category
    cars_by_category = {}
    for car in cars:
        cat = car.get('category')
        if cat:
            cars_by_category.setdefault(cat, []).append(car)

    # Merge each driver with a car of the same category
    for driver in drivers:
        if driver.get('role') == 'driver':
            driver_cat = driver.get('category')
            available_cars = cars_by_category.get(driver_cat)
            if available_cars:
                # Assign first available car and remove it from pool
                car = available_cars.pop(0)
                driver['car'] = car
            else:
                print(f"⚠️ No car available for category: {driver_cat}")
                driver['car'] = None

    # Save merged drivers
    with open(drivers_file, 'w', encoding='utf-8') as f:
        json.dump(drivers, f, indent=2, ensure_ascii=False)

    print("✅ Successfully merged cars into drivers by category!")

