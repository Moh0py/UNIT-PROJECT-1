from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="my_app")

def calculate_distance(origin: str, destination: str) -> float | None:

    try:
        loc1 = geolocator.geocode(origin, timeout=10)
        loc2 = geolocator.geocode(destination, timeout=10)
        if not loc1 or not loc2:
            print(f"Error geocoding '{origin}' or '{destination}'")
            return None
        coords_1 = (loc1.latitude, loc1.longitude)
        coords_2 = (loc2.latitude, loc2.longitude)
        # Calculate geodesic distance in kilometers
        dist_km = geodesic(coords_1, coords_2).km
        return round(dist_km, 2)
    except Exception as e:
        print(f"Distance error: {e}")
        return None
