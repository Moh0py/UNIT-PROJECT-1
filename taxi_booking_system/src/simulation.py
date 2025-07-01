import time
import argparse
from asciimatics.screen import Screen
from geopy.geocoders import Nominatim


def get_coordinates(place, geolocator):
    """Geocode a place name into (latitude, longitude)."""
    location = geolocator.geocode(place)
    if not location:
        raise ValueError(f"Cannot geocode: '{place}'")
    return (location.latitude, location.longitude)


def interpolate(route_coords, steps):
    """Generate intermediate points between waypoints."""
    points = []
    for i in range(len(route_coords) - 1):
        lat1, lon1 = route_coords[i]
        lat2, lon2 = route_coords[i + 1]
        for s in range(steps):
            t = s / steps
            lat = lat1 + t * (lat2 - lat1)
            lon = lon1 + t * (lon2 - lon1)
            points.append((lat, lon))
    points.append(route_coords[-1])
    return points


def map_to_grid(latlon_points, width, height):
    """Normalize lat/lon to fit an ASCII grid."""
    lats = [pt[0] for pt in latlon_points]
    lons = [pt[1] for pt in latlon_points]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    grid = []
    for lat, lon in latlon_points:
        x = int((lon - min_lon) / (max_lon - min_lon) * (width - 2)) + 1 if max_lon != min_lon else width // 2
        y = int((lat - min_lat) / (max_lat - min_lat) * (height - 2)) + 1 if max_lat != min_lat else height // 2
        grid.append((x, y))
    return grid


def simulate(screen, grid_points):
    """Draw and animate the driver on an ASCII grid."""
    w, h = min(screen.width, 80), min(screen.height, 24)
    for idx, (x, y) in enumerate(grid_points):
        screen.clear()
        # Draw border
        for i in range(w): screen.print_at('-', i, 0); screen.print_at('-', i, h-1)
        for j in range(h): screen.print_at('|', 0, j); screen.print_at('|', w-1, j)
        # Draw full path
        for px, py in grid_points:
            screen.print_at('.', px, py)
        # Draw driver
        screen.print_at('🚕', x, y)
        screen.print_at(f"Step {idx+1}/{len(grid_points)}", 2, h-1)
        screen.refresh()
        time.sleep(0.5)


def simulate_ascii_route(places, steps=10):
    """Main entry point: geocode, interpolate, map, and animate."""
    if not places:
        raise ValueError("No places provided for simulation.")
    if steps <= 0:
        raise ValueError("Steps must be a positive integer.")
    geolocator = Nominatim(user_agent="taxi_simulation_integration")
    route_coords = [get_coordinates(p, geolocator) for p in places]
    latlon_points = interpolate(route_coords, steps)
    Screen.wrapper(lambda scr: simulate(scr, map_to_grid(latlon_points, scr.width, scr.height)))