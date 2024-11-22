import tkinter as tk
from tkinter import Label, Scale, HORIZONTAL
import ctypes
import winreg

# Function to get primary monitor details
def get_monitor_details():
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    # Set DPI awareness to get accurate resolution on high-DPI displays
    user32.SetProcessDPIAware()

    # Get screen resolution
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    resolution = f"{screen_width}x{screen_height}"

    # Get color depth (bits per pixel)
    hdc = user32.GetDC(0)
    bits_per_pixel = gdi32.GetDeviceCaps(hdc, 12)  # 12 is the index for bits per pixel
    color_depth = f"{bits_per_pixel} bit"

    # Get monitor DPI (dots per inch)
    dpi = gdi32.GetDeviceCaps(hdc, 88)  # 88 is the index for horizontal DPI
    dpi_text = f"{dpi} DPI"

    # Get monitor model from the Windows Registry
    monitor_name = "Unknown"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"SYSTEM\CurrentControlSet\Enum\DISPLAY") as reg_key:
            first_subkey = winreg.EnumKey(reg_key, 0)
            with winreg.OpenKey(reg_key, f"{first_subkey}\\Device Parameters") as device_params:
                monitor_name, _ = winreg.QueryValueEx(device_params, "FriendlyName")
    except FileNotFoundError:
        pass  # If not found, keep "Unknown" as default

    # Build monitor details string
    details = (f"Monitor Model: {monitor_name}\nResolution: {resolution}\n"
               f"Color Depth: {color_depth}\nDPI: {dpi_text}\nBrightness: {get_brightness()}%")
    return details

# Function to get current brightness level
def get_brightness():
    try:
        # Access the WMI to get monitor brightness if available
        wmi = ctypes.windll.LoadLibrary('wbemuuid.dll')
        brightness = ctypes.c_uint()
        ctypes.windll.powrprof.GetMonitorBrightness(0, ctypes.byref(brightness))
        return brightness.value
    except:
        return 50  # Return a default value if brightness isn't accessible

# Function to set brightness (range 0-100)
def set_brightness(value):
    try:
        brightness = int(value)
        hdc = ctypes.windll.gdi32.GetDC(0)
        ctypes.windll.dxva2.SetMonitorBrightness(hdc, brightness)
    except:
        print("Brightness adjustment not supported on this device.")

# Set up the main window
root = tk.Tk()
root.title("Monitor Info Viewer")
root.geometry("400x300")

# Label to display monitor info
info_label = Label(root, text=get_monitor_details(), font=("Arial", 10), justify="left")
info_label.pack(pady=10)

# Brightness adjustment slider
brightness_label = Label(root, text="Adjust Brightness:", font=("Arial", 10))
brightness_label.pack(pady=5)

# Ensure brightness is numeric before setting
brightness_level = get_brightness()
brightness_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_brightness)
brightness_slider.set(brightness_level)  # Set to current brightness level
brightness_slider.pack()

# Button to refresh info
def update_info():
    info_label.config(text=get_monitor_details())

refresh_button = tk.Button(root, text="Refresh", command=update_info)
refresh_button.pack(pady=10)

# Run the application
root.mainloop()
