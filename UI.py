import json
import tkinter as tk
from tkinter import messagebox

CONFIG_FILE = "settings.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If config file does not exist, create one with default values
        default_config = {
            "cursor_sensitivity": 1.0,
            "scroll_delay": 0.5,
            "scroll_amount": 120,
            "zoom_amount": 50
        }
        save_config(default_config)
        return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def update_config(cursor_sensitivity, scroll_delay, scroll_amount, zoom_amount):
    try:
        config = {
            "cursor_sensitivity": float(cursor_sensitivity.get()),
            "scroll_delay": float(scroll_delay.get()),
            "scroll_amount": int(scroll_amount.get()),
            "zoom_amount": int(zoom_amount.get())
        }
        save_config(config)
        messagebox.showinfo("Info", "Configuration saved successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values.")
def launch_config_ui():
    app = tk.Tk()
    app.title("Configuration")

    tk.Label(app, text="Cursor Sensitivity:").grid(row=0, column=0, padx=10, pady=5)
    cursor_sensitivity = tk.Entry(app)
    cursor_sensitivity.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(app, text="Scroll Delay (seconds):").grid(row=1, column=0, padx=10, pady=5)
    scroll_delay = tk.Entry(app)
    scroll_delay.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(app, text="Scroll Amount:").grid(row=2, column=0, padx=10, pady=5)
    scroll_amount = tk.Entry(app)
    scroll_amount.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(app, text="Zoom Amount:").grid(row=3, column=0, padx=10, pady=5)
    zoom_amount = tk.Entry(app)
    zoom_amount.grid(row=3, column=1, padx=10, pady=5)

    config = load_config()
    cursor_sensitivity.insert(0, config.get("cursor_sensitivity", 1.0))
    scroll_delay.insert(0, config.get("scroll_delay", 0.5))
    scroll_amount.insert(0, config.get("scroll_amount", 120))
    zoom_amount.insert(0, config.get("zoom_amount", 50))

    tk.Button(app, text="Save", command=lambda: update_config(cursor_sensitivity,scroll_delay,scroll_amount,zoom_amount)).grid(row=4, column=0, columnspan=2, pady=10)

    app.mainloop()
