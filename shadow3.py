import math
from datetime import datetime, timedelta
from astral.location import Observer
from astral.sun import elevation, azimuth
import pytz

def print_shadow_oct5(city_name="Beijing", height_m=1.57):
    # Hardcoded coordinates
    CITY_COORDS = {
        "Beijing": (39.9042, 116.4074),
        "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060),
    }
    lat, lon = CITY_COORDS.get(city_name, (39.9042, 116.4074))
    tz = pytz.timezone("Asia/Shanghai")
    observer = Observer(latitude=lat, longitude=lon)

    # Time range: Oct 5th, 00:00 → 23:00, step 1 hour
    start = tz.localize(datetime(2025, 10, 5, 0, 0))
    end = tz.localize(datetime(2025, 10, 5, 23, 0))
    step = timedelta(hours=1)
    current = start

    print(f"Shadow lengths and angles for {city_name} on 2025-10-05 (height={height_m} m):\n")
    print(f"{'Datetime':<20} | {'Length (m)':>10} | {'Angle (°)':>10}")
    print("-" * 45)

    while current <= end:
        alt = elevation(observer, current)
        azi = azimuth(observer, current)
        if alt > 0:
            shadow_length = height_m / math.tan(math.radians(alt))
            shadow_angle = (azi + 180) % 360  # direction opposite to sun
        else:
            shadow_length = float('inf')  # sun below horizon
            shadow_angle = None
        angle_str = f"{shadow_angle:.2f}" if shadow_angle is not None else "N/A"
        print(f"{current.strftime('%Y-%m-%d %H:%M'):<20} | {shadow_length:>10.2f} | {angle_str:>10}")
        current += step

if __name__ == "__main__":
    print_shadow_oct5("Beijing", height_m=1.57)
