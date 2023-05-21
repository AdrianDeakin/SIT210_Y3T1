import random
import tkinter as tk
import datetime
from tkinter import messagebox
import time
import subprocess
from particle import Particle
import os
from PIL import ImageGrab
from particle import *
import time
import subprocess

# Particle credentials
PARTICLE_USERNAME = "wongadr@deakin.edu.au"
PARTICLE_PASSWORD = "95923593aP"
PARTICLE_DEVICE_ID = "eOOfce68c2837cfd37988df8"

# Create a new Particle API client
particle = Particle(pdgid=123, pdg_name='221262257')
#particle = Particle(username=PARTICLE_USERNAME, password=PARTICLE_PASSWORD)

# THE MAIN WINDOW
root = tk.Tk()
root.title("Smart Plant Monitoring System")
root.geometry("700x590")

# Define the comfortable ranges for the data values
temp_range = (15, 24)
humid_range = (40, 60)
light_range = (10, 30)
moisture_range = (40, 60)

# Empty list to store sensor data
sensor_data = []

# Function to update the data values
def update_data():
    
    temperatures = [round(random.uniform(17, 19), 1) for _ in range(5)]
    temperature = round(sum(temperatures)/len(temperatures), 1)
    temperature_str = str(temperature) + " °C"

    humidities = [round(random.uniform(38, 42), 1) for _ in range(5)]
    humidity = round(sum(humidities)/len(humidities), 1)
    humidity_str = str(humidity) + " %"
    
    lights = [round(random.uniform(10, 11), 1) for _ in range(5)]
    light = round(sum(lights)/len(lights), 1)
    light_str = str(light) + " lux"
    
    moistures = [round(random.uniform(38, 42), 1) for _ in range(5)]
    moisture = round(sum(moistures)/len(moistures), 1)
    moisture_str = str(moisture) + " %"

    # Append the current sensor data to the list
    sensor_data.append((temperature, humidity, light, moisture))

    # Slice the last 5 items to get the average values of the past 5 minutes
    sensor_data_last_5_min = sensor_data[-5:]
    temperature = round(sum([d[0] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    humidity = round(sum([d[1] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    light = round(sum([d[2] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    moisture = round(sum([d[3] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)

    # Update the labels with the new data
    temp_label.config(text=str(temperature) + " °C")
    humid_label.config(text=str(humidity) + " %")
    light_label.config(text=str(light) + " lux")
    moisture_label.config(text=str(moisture) + " %")

    # Change the text color based on whether the value is within range or not
    if temperature < temp_range[0] or temperature > temp_range[1]:
        temp_label.config(fg="red")
    else:
        temp_label.config(fg="green")

    if humidity < humid_range[0] or humidity > humid_range[1]:
        humid_label.config(fg="red")
    else:
        humid_label.config(fg="green")

    if light < light_range[0] or light > light_range[1]:
        light_label.config(fg="red")
    else:
        light_label.config(fg="green")

    if moisture < moisture_range[0] or moisture > moisture_range[1]:
        moisture_label.config(fg="red")
    else:
        moisture_label.config(fg="green")

    # Schedule the function to run again in 24 seconds
    root.after(24000, update_data)

# Submit Version for Update Data Function
"""def update_data():
    # Call the particle serial monitor command to get the sensor data
    # Assumes that the particle CLI is installed and the device is connected via USB
    output = subprocess.check_output(['particle', 'serial', 'monitor']).decode('utf-8')

    # Parse the output to extract the temperature, humidity, light, and moisture values
    lines = output.strip().split('\n')
    data_line = None
    for line in lines:
        if 'Data:' in line:
            data_line = line
            break
    if data_line is None:
        print('No data received from device')
        return
    data_str = data_line.split(': ')[1]
    temperature, humidity, light, moisture = map(float, data_str.split(','))

    # Format the values as strings with units
    temperature_str = f'{temperature:.1f} °C'
    humidity_str = f'{humidity:.1f} %'
    light_str = f'{light:.1f} lux'
    moisture_str = f'{moisture:.1f} %'

    # Append the current sensor data to the list
    sensor_data.append((temperature, humidity, light, moisture))

    # Slice the last 5 items to get the average values of the past 5 minutes
    sensor_data_last_5_min = sensor_data[-5:]
    temperature = round(sum([d[0] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    humidity = round(sum([d[1] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    light = round(sum([d[2] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)
    moisture = round(sum([d[3] for d in sensor_data_last_5_min])/len(sensor_data_last_5_min), 1)

    # Update the labels with the new data
    temp_label.config(text=str(temperature) + " °C")
    humid_label.config(text=str(humidity) + " %")
    light_label.config(text=str(light) + " lux")
    moisture_label.config(text=str(moisture) + " %")

    # Change the text color based on whether the value is within range or not
    if temperature < temp_range[0] or temperature > temp_range[1]:
        temp_label.config(fg="red")
    else:
        temp_label.config(fg="green")

    if humidity < humid_range[0] or humidity > humid_range[1]:
        humid_label.config(fg="red")
    else:
        humid_label.config(fg="green")

    if light < light_range[0] or light > light_range[1]:
        light_label.config(fg="red")
    else:
        light_label.config(fg="green")

    if moisture < moisture_range[0] or moisture > moisture_range[1]:
        moisture_label.config(fg="red")
    else:
        moisture_label.config(fg="green")

    # LED on board
    red_led_pin = "D0"
    green_led_pin = "D1"
    if temperature < temp_range[0] or temperature > temp_range[1] or \
   humidity < humid_range[0] or humidity > humid_range[1] or \
   light < light_range[0] or light > light_range[1] or \
   moisture < moisture_range[0] or moisture > moisture_range[1]:
        particle.digitalWrite(red_led_pin, particle.HIGH)
        particle.digitalWrite(green_led_pin, particle.LOW)
    else:
        particle.digitalWrite(red_led_pin, particle.LOW)
        particle.digitalWrite(green_led_pin, particle.HIGH)

    # Schedule the function to run again in 24 seconds
    root.after(24000, update_data)"""

# Function to genrate report
def generate_report():
    # Create a pop up window for the report
    report_window = tk.Toplevel(root)
    report_window.title("REPORT")

    top_area = tk.Frame(report_window, bg="#b39ddb", height=70)
    top_area.pack(side="top", fill="both", expand=True)
    top_text = tk.Label(top_area, text="Plant Monitor Report", font=("Helvetica", 20, "bold"), bg="#b39ddb", fg="white")
    top_text.place(relx=0.5, rely=0.5, anchor="center")
    bottom_area = tk.Frame(report_window, bg="#986fde", height=70)
    bottom_area.pack(side="bottom", fill="both", expand=True)
    
    # Calculate the average data of each sensor in the past 5 minutes
    temp_sum, humid_sum, light_sum, moisture_sum = 0, 0, 0, 0
    num_samples = 0
    for sample in sensor_data[-5:]:
        temp_sum += sample[0]
        humid_sum += sample[1]
        light_sum += sample[2]
        moisture_sum += sample[3]
        num_samples += 1
    if num_samples > 0:
        temp_avg = round(temp_sum / num_samples, 1)
        humid_avg = round(humid_sum / num_samples, 1)
        light_avg = round(light_sum / num_samples, 1)
        moisture_avg = round(moisture_sum / num_samples, 1)
    else:
        temp_avg, humid_avg, light_avg, moisture_avg = 0, 0, 0, 0

    # Add the average data to the report
    report_data = ["Average value of data collected:",
                   "Temperature: {}°C".format(temp_avg),
                   "Humidity: {}%".format(humid_avg),
                   "Light / 100: {} lux".format(light_avg),
                   "Moisture: {}%".format(moisture_avg),
                   "---------------------------------------------------------------------------------------------------"]
    for data in report_data:
        data_label = tk.Label(report_window, text=data, font=("Helvetica", 16))
        data_label.pack(pady=5)

    # Suggest actions based on the average data
    report_data2 = ["Suggested Actions:"]

    if temp_avg < temp_range[0]:
        report_data2.append(" - Increase temperature by providing a heat source.")
    elif temp_avg > temp_range[1]:
        report_data2.append(" - Decrease temperature by providing a cooling source.")

    if humid_avg < humid_range[0]:
        report_data2.append(" - Increase humidity by misting or using a humidifier.")
    elif humid_avg > humid_range[1]:
        report_data2.append(" - Decrease humidity by improving ventilation or using a dehumidifier.")

    if light_avg < light_range[0]:
        report_data2.append(" - Increase light by moving the plant closer to a window or using artificial light.")
    elif light_avg > light_range[1]:
        report_data2.append(" - Decrease light by moving the plant away from direct sunlight or using shades.")

    if moisture_avg < moisture_range[0]:
        report_data2.append(" - Water the plant more frequently.")
    elif moisture_avg > moisture_range[1]:
        report_data2.append(" - Water the plant less frequently.")

    for data in report_data2:
        data_label = tk.Label(report_window, text=data, font=("Helvetica", 16))
        data_label.pack(pady=5)

    # Add a refresh button to update the report
    def refresh_report():
        report_window.destroy()
        generate_report()

    def send_report_email():
        event_name = "plant_report_email_function"
        event_data = "1"
        subprocess.run(["particle", "publish", event_name, event_data])
        messagebox.showinfo("Email Sent", "Email has been sent. Please check your mailbox.")
    
    # report window menu bar
    menu_bar = tk.Menu(report_window)
    menu_bar.add_command(label="Refresh Report", command=refresh_report)
    menu_bar.add_command(label="Email the Report", command=send_report_email)
    menu_bar.add_command(label="Close Report", command=report_window.destroy)
    report_window.config(menu=menu_bar)

# Function to ask for confirm when exit program
def confirm_exit():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

def generate_chart():
    # Create a pop up window for the chart
    chart_window = tk.Toplevel(root)
    chart_window.title("CHART")
    
    top_area = tk.Frame(chart_window, bg="#b39ddb", height=70)
    top_area.pack(side="top", fill="both", expand=True)
    top_text = tk.Label(top_area, text="Data Trend of the plant", font=("Helvetica", 20, "bold"), bg="#b39ddb", fg="white")
    top_text.place(relx=0.5, rely=0.5, anchor="center")
    bottom_area = tk.Frame(chart_window, bg="#986fde", height=70)
    bottom_area.pack(side="bottom", fill="both", expand=True)

    # Create a canvas for the chart
    chart_canvas = tk.Canvas(chart_window, width=800, height=400, bg="white")
    chart_canvas.pack()

    # Calculate the x and y coordinates for the data points
    x_spacing = 700 / len(sensor_data)
    x_coord = 50
    y_scale = 2
    temp_points = []
    humid_points = []
    light_points = []
    moisture_points = []
    for sample in sensor_data:
        temp_points.append((x_coord, 350 - (sample[0] * y_scale)))
        humid_points.append((x_coord, 350 - (sample[1] * y_scale)))
        light_points.append((x_coord, 350 - (sample[2] * y_scale)))
        moisture_points.append((x_coord, 350 - (sample[3] * y_scale)))
        x_coord += x_spacing

    # Draw the x and y axes
    chart_canvas.create_line(50, 160, 50, 350, width=3)  # y-axis
    chart_canvas.create_line(50, 350, 750, 350, width=3)  # x-axis

    # Add labels to the y-axis
    chart_canvas.create_text(20, 190, text="60", anchor="e")
    chart_canvas.create_text(20, 230, text="45", anchor="e")
    chart_canvas.create_text(20, 270, text="30", anchor="e")
    chart_canvas.create_text(20, 310, text="15", anchor="e")
    chart_canvas.create_text(20, 350, text="0", anchor="e")

    # Draw the line
    chart_canvas.create_line(temp_points, fill="red", width=2)
    chart_canvas.create_line(humid_points, fill="blue", width=2)
    chart_canvas.create_line(light_points, fill="green", width=2)
    chart_canvas.create_line(moisture_points, fill="purple", width=2)

    # Add a label to show text at the bottom
    text_label = tk.Label(chart_window, text="The red line stand for temperature", font=("Helvetica", 11), fg="red")
    text_label.pack(pady=10)

    text_label = tk.Label(chart_window, text="The blue line stand for humidity", font=("Helvetica", 11), fg="blue")
    text_label.pack(pady=10)

    text_label = tk.Label(chart_window, text="The green line stand for light / 100", font=("Helvetica", 11), fg="Green")
    text_label.pack(pady=10)

    text_label = tk.Label(chart_window, text="The purple line stand for moisture", font=("Helvetica", 11), fg="purple")
    text_label.pack(pady=10)

    # Add a close button to close the chart window
    # close_button = tk.Button(chart_window, text="Close Chart", command=chart_window.destroy)
    # close_button.pack(side="bottom", pady=10)

    # Add a refresh button to update the report
    def refresh_chart():
        chart_window.destroy()
        generate_chart()

    # chart window menu bar
    menu_bar = tk.Menu(chart_window)
    menu_bar.add_command(label="Refresh Chart", command=refresh_chart)
    menu_bar.add_command(label="Close Chart", command=chart_window.destroy)
    chart_window.config(menu=menu_bar)

# Configure row and column weights for the root widget
root.grid_columnconfigure(0, weight=1)
# root.grid_rowconfigure(0, weight=1)

# Menu Window Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_bar.add_command(label="Refresh Data Now", command=update_data)
menu_bar.add_command(label="Genrate Report", command=generate_report)
menu_bar.add_command(label="Genrate Chart", command=generate_chart)
menu_bar.add_command(label="Exit", command=confirm_exit)

#Main Window Top and Bottom Bar
top_area = tk.Frame(root, bg="#b39ddb", height=70)
top_area.grid(row=0, column=0, columnspan=2, sticky="nsew")
system_name_label = tk.Label(root, text="Smart Plant Monitoring System", font=("Helvetica", 30, "bold"), bg="#b39ddb", fg="white")
system_name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
bottom_area = tk.Frame(root, bg="#986fde", height=70)
bottom_area.grid(row=7, column=0, columnspan=2, sticky="nsew")

# Labels for the 4 data values
tk.Label(root, text="Temperature :", font=("Helvetica", 40, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
temp_label = tk.Label(root, text="", font=("Helvetica", 40, "bold"))
temp_label.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")

tk.Label(root, text="Humidity :", font=("Helvetica", 40, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="nswe")
humid_label = tk.Label(root, text="", font=("Helvetica", 40, "bold"))
humid_label.grid(row=2, column=1, padx=10, pady=10, sticky="nswe")

tk.Label(root, text="Light / 100 :", font=("Helvetica", 40, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="nswe")
light_label = tk.Label(root, text="", font=("Helvetica", 40, "bold"))
light_label.grid(row=3, column=1, padx=10, pady=10, sticky="nswe")

tk.Label(root, text="Soil Moisture :", font=("Helvetica", 40, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="nswe")
moisture_label = tk.Label(root, text="", font=("Helvetica", 40, "bold"))
moisture_label.grid(row=4, column=1, padx=10, pady=10, sticky="nswe")

# Main Window Exit button
exit_button = tk.Button(root, text="Exit Program", command=confirm_exit, font=("Helvetica", 20), bg="red", fg="white")
exit_button.grid(row=6, column=0, columnspan=2, pady=20, padx=100, sticky="nswe")

# Schedule the function to run for the first time
root.after(0, update_data)

# Start the main event loop
root.mainloop()