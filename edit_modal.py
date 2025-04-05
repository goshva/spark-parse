import tkinter as tk
from tkinter import messagebox
import webbrowser
import urllib.parse

class EditModal:
    def __init__(self, parent, item_id, current_values, save_callback):
        self.edit_window = tk.Toplevel(parent)
        self.edit_window.title("Edit Company")
        self.item_id = item_id
        self.save_callback = save_callback

        # Fields and their corresponding current values
        self.fields = ["Company Name", "Latitude", "Longitude", "Caption", "Address", "Link", "OGRN", "INN", "OKPO", "Rating", "Yandex Rating (0-9)", "2GIS Rating (0-9)", "Otzovik Rating (0-9)", "Phone", "Site URL", "Email"]
        self.entries = {}

        for i, field in enumerate(self.fields):
            tk.Label(self.edit_window, text=field).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = tk.Entry(self.edit_window)
            entry.insert(0, current_values[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Save button
        save_button = tk.Button(self.edit_window, text="Save Changes", command=self.save_changes)
        save_button.grid(row=len(self.fields), column=0, pady=10)

        # Yandex Maps button
        maps_button = tk.Button(self.edit_window, text="Open in Yandex Maps", command=self.open_yandex_maps)
        maps_button.grid(row=len(self.fields), column=1, pady=10)

    def save_changes(self):
        try:
            new_values = [
                self.entries["Company Name"].get(),
                float(self.entries["Latitude"].get()),
                float(self.entries["Longitude"].get()),
                self.entries["Caption"].get(),
                self.entries["Address"].get(),
                self.entries["Link"].get(),
                self.entries["OGRN"].get(),
                self.entries["INN"].get(),
                self.entries["OKPO"].get(),
                float(self.entries["Rating"].get()),
                int(self.entries["Yandex Rating (0-9)"].get()),
                int(self.entries["2GIS Rating (0-9)"].get()),
                int(self.entries["Otzovik Rating (0-9)"].get()),
                self.entries["Phone"].get(),
                self.entries["Site URL"].get(),
                self.entries["Email"].get()
            ]

            # Validate rating fields
            if not (0 <= new_values[10] <= 9):
                raise ValueError("Yandex Rating must be between 0 and 9.")
            if not (0 <= new_values[11] <= 9):
                raise ValueError("2GIS Rating must be between 0 and 9.")
            if not (0 <= new_values[12] <= 9):
                raise ValueError("Otzovik Rating must be between 0 and 9.")

            self.save_callback(self.item_id, new_values)
            self.edit_window.destroy()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def open_yandex_maps(self):
        company_name = urllib.parse.quote(self.entries["Company Name"].get())
        url = f"https://yandex.ru/maps/11062/kislovodsk/search/{company_name}/?ll=42.706534%2C43.919944&sll=42.706534%2C43.915673&sspn=0.104971%2C0.044052&z=13"
        webbrowser.open(url)
