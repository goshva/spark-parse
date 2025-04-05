import tkinter as tk
from tkinter import ttk, messagebox
import urllib.parse
import webbrowser

class EditModal:
    def __init__(self, parent, item_id, current_values, save_callback):
        self.parent = parent
        self.item_id = item_id
        self.current_values = current_values
        self.save_callback = save_callback

        self.modal = tk.Toplevel(parent)
        self.modal.title("Edit Company")

        self.fields = ["Company Name", "Latitude", "Longitude", "Caption", "Address", "Link", "OGRN", "INN", "OKPO", "Rating", "Yandex", "2GIS", "Otzovik", "Phone", "Site URL", "Email"]
        self.entries = {}

        for i, field in enumerate(self.fields):
            label = ttk.Label(self.modal, text=field)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            value = self.parse_float(current_values[i]) if field in ["Latitude", "Longitude", "Rating", "Yandex", "2GIS", "Otzovik"] else current_values[i]
            entry = ttk.Entry(self.modal)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Add the button for opening Yandex Maps
        yandex_button = ttk.Button(self.modal, text="Open in Yandex Maps", command=self.open_yandex_maps)
        yandex_button.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(self.modal, text="Save", command=self.save)
        save_button.grid(row=len(self.fields) + 2, column=0, columnspan=2, pady=10)

    def parse_float(self, value):
        if value is None or value == '':
            return 0.0  # or any default value you prefer
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            return 0.0  # or any default value you prefer

    def open_yandex_maps(self):
        company_name = urllib.parse.quote(self.entries["Company Name"].get())
        url = f"https://yandex.ru/maps/11062/kislovodsk/search/{company_name}/?ll=42.706534%2C43.919944&sll=42.706534%2C43.915673&sspn=0.104971%2C0.044052&z=13"
        webbrowser.open(url)

    def save(self):
        new_values = [self.entries[field].get() for field in self.fields]
        self.save_callback(self.item_id, new_values)
        self.modal.destroy()
