# required modules
import requests
import tkinter as tk


def get_data():
    endpoint = "current.json"
    api_key = "42cdda6c8c894dc0b23122828240906"
    location = str(entry.get()).lower()

    url = f"http://api.weatherapi.com/v1/{endpoint}?key={api_key}&q={location}"
    resp = requests.get(url)
    data = resp.json()
    """ required data:
        data['current']['parameter'] 
        parameters:
            temp_c
            humidity
            wind_kph
            precip_mm
            pressure_mb
    """
    update_output(data=data,status_code=resp.status_code)


def update_output(data, status_code):
    if status_code == 200:
        text = [
            data['current']['temp_c'],
            data['current']['humidity'],
            data['current']['wind_kph'],
            data['current']['precip_mm'],
            data['current']['pressure_mb']
            ] 
    else:
        text = ['','','','','']
    temperature.config(text=f"Temperature\t: {text[0]}\t c\t")
    humidity.config(text=f"Humidity\t\t: {text[1]}\t %\t")
    wind_speed.config(text=f"Wind speed\t: {text[2]}\t km/h\t")
    precipitation.config(text=f"Precipitation\t: {text[3]}\t mb\t")
    pressure.config(text=f"Pressure\t\t: {text[4]}\t kpa\t")


# => Implement GUI

root = tk.Tk()
root.title("Weather Forecast")
root.resizable(width=False, height=False)


""" input field frame
position (row=0, col=0)
Element:
    label, entry, button (0, 0-2)
"""
input_field = tk.Frame(root, padx=20, pady=20)
input_field.grid(row=0,column=0)

lbl1 = tk.Label(input_field, text="Enter the location")
lbl1.grid(row=0,column=0)

entry = tk.Entry(input_field)
entry.grid(row=0,column=1)

btn = tk.Button(input_field, text="search", command=get_data)
btn.grid(row=0,column=2)


""" output field frame
position (row=1, col=0)
Elements:
    5 labels for parameters results (0-4, 1)
"""
output_field = tk.Frame(root, padx=20, pady=20)
output_field.grid(row=1,column=0)

temperature = tk.Label(output_field,text="Temperature\t")
temperature.grid(row=0, column=0)
humidity = tk.Label(output_field,text="Humidity\t\t")
humidity.grid(row=1, column=0)
wind_speed = tk.Label(output_field,text="Wind speed\t")
wind_speed.grid(row=2, column=0)
precipitation = tk.Label(output_field,text="Precipitation\t")
precipitation.grid(row=3, column=0)
pressure = tk.Label(output_field,text="Pressure\t\t")
pressure.grid(row=4, column=0)

root.mainloop()
