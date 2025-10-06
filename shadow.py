from astral import LocationInfo
from astral.sun import sun, elevation, azimuth
from astral.location import Observer
from datetime import datetime
import pytz
import math
import matplotlib.pyplot as plt

def get_shadow(city_name, height_m, time_str):
    # hardcode known coordinates (avoid network)
    CITY_COORDS = {
        "Beijing": (39.9042, 116.4074),
        "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060),
        "London": (51.5074, -0.1278),
    }

    lat, lon = CITY_COORDS.get(city_name, (None, None))
    if lat is None:
        raise ValueError(f"Unknown city '{city_name}' — please add coordinates.")

    city = LocationInfo(name=city_name, region="", timezone="Asia/Shanghai",
                        latitude=lat, longitude=lon)

    # time zone aware datetime
    local_tz = pytz.timezone(city.timezone)
    dt = local_tz.localize(datetime.fromisoformat(time_str))

    # Astral v3+ way to compute sun position
    observer = Observer(latitude=lat, longitude=lon)
    alt = elevation(observer, dt)
    azi = azimuth(observer, dt)

    if alt <= 0:
        print("🌙 The sun is below the horizon — no visible shadow.")
        return

    # compute shadow length and direction
    shadow_length = height_m / math.tan(math.radians(alt))
    shadow_dir = (azi + 180) % 360  # opposite to the sun

    print(f"📍 City: {city_name}")
    print(f"🕒 Time: {dt}")
    print(f"☀️ Sun altitude: {alt:.2f}°")
    print(f"🧭 Sun azimuth: {azi:.2f}°")
    print(f"➡️ Shadow direction: {shadow_dir:.2f}° (clockwise from north)")
    print(f"📏 Shadow length: {shadow_length:.2f} m")

    # plot
    plt.figure(figsize=(5, 5))
    plt.title(f"Shadow in {city_name}\n{dt.strftime('%Y-%m-%d %H:%M')}")
    plt.scatter(0, 0, color='orange', label='Person')
    x = shadow_length * math.sin(math.radians(shadow_dir))
    y = shadow_length * math.cos(math.radians(shadow_dir))
    plt.arrow(0, 0, x, y, head_width=0.2, length_includes_head=True, color='gray')
    plt.text(x / 2, y / 2, f"{shadow_length:.2f} m", fontsize=10)
    plt.xlabel("East (m)")
    plt.ylabel("North (m)")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()

# Example
if __name__ == "__main__":
    get_shadow("Beijing", height_m=1.54, time_str="2025-10-06T15:00:00")

