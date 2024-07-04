import tkinter as tk
import requests
import json

# Replace with your actual API key
api_key = "42cdda6c8c894dc0b23122828240906"

def get_weather(location):
    """Fetches weather data from the API and returns it as a dictionary."""
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "temp_c": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "precip_mm": data["current"]["precip_mm"] if data["current"].get("precip_mm") else 0,  # Handle potential missing data
            "pressure_mb": data["current"]["pressure_mb"],
        }
    else:
        # Handle API errors and location not found cases
        if response.status_code == 400:  # Likely invalid location
            return {"error": "No matching location found"}
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}

def update_weather(location):
    """Fetches weather data and updates the GUI labels, displaying specific error message."""
    weather_data = get_weather(location.get())

    if "error" in weather_data:
        error_label.config(text=weather_data["error"], fg="red")
        # Clear weather labels on error (optional)
        temp_label.config(text="")
        humidity_label.config(text="")
        wind_label.config(text="")
        precip_label.config(text="")
        pressure_label.config(text="")
    else:
        error_label.config(text="")
        # Update weather labels with consistent formatting
        temp_label.config(text=f"Temperature: {weather_data['temp_c']}°C")
        humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        wind_label.config(text=f"Wind Speed: {weather_data['wind_kph']} kph")
        precip_label.config(text=f"Precipitation: {weather_data['precip_mm']} mm")
        pressure_label.config(text=f"Pressure: {weather_data['pressure_mb']} mb")

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("400x400")  # Set fixed window size
root.resizable(False, False)  # Disables resizing

# Label for location input
location_label = tk.Label(root, text="Enter Location:", font=("Arial", 12))
location_label.pack(pady=5)

# Input field
location_entry = tk.Entry(root, width=30, font=("Arial", 16))
location_entry.pack(pady=10)

# Get weather button
get_weather_button = tk.Button(root, text="Get Weather", command=lambda: update_weather(location_entry), font=("Arial", 14))
get_weather_button.pack(pady=5)

# Error label (centered for better display)
error_label = tk.Label(root, text="", fg="red", font=("Arial", 14))
error_label.pack(pady=5)

# Weather information labels (with consistent formatting)
temp_label = tk.Label(root, text="", font=("Arial", 16))
temp_label.pack()

humidity_label = tk.Label(root, text="", font=("Arial", 16))
humidity_label.pack()

wind_label = tk.Label(root, text="", font=("Arial", 16))
wind_label.pack()

precip_label = tk.Label(root, text="", font=("Arial", 16))
precip_label.pack()

pressure_label = tk.Label(root, text="", font=("Arial", 16))
pressure_label.pack()

root.mainloop()
