
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

url = "http://10.57.250.162:80"

timestamps = []
temps = []
hums = []

# Create figure and 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

def update(frame):
    global timestamps, temps, hums

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        p_tags = soup.find_all("p")

        temp = None
        hum = None

        for p in p_tags:
            text = p.get_text(strip=True)
            if "Temperature" in text:
                temp = float(text.split(":")[1].strip().split()[0])
            elif "Humidity" in text:
                hum = float(text.split(":")[1].strip().split()[0])

        if temp is not None and hum is not None:
            time_now = datetime.now().strftime("%H:%M:%S")
            timestamps.append(time_now)
            temps.append(temp)
            hums.append(hum)

            # Keep only last 50 points
            timestamps[:] = timestamps[-50:]
            temps[:] = temps[-50:]
            hums[:] = hums[-50:]

            # Clear and plot Temp
            ax1.clear()
            ax1.plot(timestamps, temps, color='red', label='Temperature (°C)')
            ax1.set_ylabel("Temperature (°C)")
            ax1.set_ylim(15, 27)
            ax1.set_yticks(np.arange(15, 27, 0.6))
            ax1.grid(True, linestyle='--', alpha=0.5)
            ax1.legend(loc="upper left")

            # Clear and plot Humidity
            ax2.clear()
            ax2.plot(timestamps, hums, color='blue', label='Humidity (%)')
            ax2.set_ylabel("Humidity (%)")
            ax2.set_ylim(0, 100)
            ax2.set_yticks(np.arange(0, 100,5))
            ax2.set_xlabel("Time")
            ax2.grid(True, linestyle='--', alpha=0.5)
            ax2.legend(loc="upper left")

            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    except Exception as e:
        print("Error:", e)

# Set up animation
ani = animation.FuncAnimation(fig, update, interval=3000)  # every 5 seconds

plt.tight_layout()
plt.show()
