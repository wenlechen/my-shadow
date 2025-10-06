import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.location import Observer
from astral.sun import elevation, azimuth
import pytz

def make_shadow_animation(city_name="Beijing", height_m=1.7):
    # Hardcoded city coordinates
    CITY_COORDS = {
        "Beijing": (39.9042, 116.4074),
        "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060),
    }
    lat, lon = CITY_COORDS.get(city_name, (39.9042, 116.4074))

    # City info
    city = LocationInfo(city_name, "", "Asia/Shanghai", lat, lon)
    tz = pytz.timezone(city.timezone)
    observer = Observer(latitude=lat, longitude=lon)

    # Time range: Oct 1st 06:00 → Oct 8th 18:00
    start = tz.localize(datetime(2025, 10, 1, 6, 0))
    end = tz.localize(datetime(2025, 10, 8, 18, 0))
    step = timedelta(minutes=30)
    times = []
    current = start
    while current <= end:
        times.append(current)
        current += step

    # Precompute shadow data
    shadows = []
    for t in times:
        alt = elevation(observer, t)
        azi = azimuth(observer, t)
        if alt > 0:
            length = height_m / math.tan(math.radians(alt))
            dir_deg = (azi + 180) % 360
            x = length * math.sin(math.radians(dir_deg))
            y = length * math.cos(math.radians(dir_deg))
        else:
            x = y = length = None  # sun below horizon
        shadows.append((x, y, length, t, alt))

    # Matplotlib setup
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_xlabel("East (m)")
    ax.set_ylabel("North (m)")
    title = ax.set_title("")
    shadow_length_text = ax.text(0, -18, "", fontsize=12, ha="center")

    person_dot, = ax.plot(0, 0, 'o', color='orange', label='Person')
    shadow_line, = ax.plot([], [], color='gray', lw=2, label='Shadow')

    def update(frame):
        x, y, length, t, alt = shadows[frame]
        if x is None:
            shadow_line.set_data([], [])
            shadow_length_text.set_text("Sun below horizon")
            title.set_text(f"{t.strftime('%Y-%m-%d %H:%M')}")
        else:
            shadow_line.set_data([0, x], [0, y])
            shadow_length_text.set_text(f"Shadow length: {length:.2f} m")
            title.set_text(
                f"{city_name}  {t.strftime('%Y-%m-%d %H:%M')}\nSun altitude={alt:.1f}°"
            )
        return shadow_line, shadow_length_text, title

    ani = FuncAnimation(
        fig, update, frames=len(times), interval=100, blit=False, repeat=False
    )

    plt.legend()
    plt.show()

    # Optional: save to mp4
    # ani.save("shadow_animation.mp4", writer="ffmpeg", fps=10)

if __name__ == "__main__":
    make_shadow_animation("Beijing", height_m=1.57)
