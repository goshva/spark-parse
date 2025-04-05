import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from edit_modal import EditModal

# Connect to the existing SQLite database
conn = sqlite3.connect('companies.db')
cursor = conn.cursor()

# Ensure the table structure is as expected and add new columns if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    place_id TEXT,
    latitude REAL,
    longitude REAL,
    caption TEXT,
    address TEXT,
    link TEXT,
    company_name TEXT,
    ogrn TEXT,
    inn TEXT,
    okpo TEXT,
    rating REAL,
    bissnes_yandex INTEGER CHECK(bissnes_yandex >= 0 AND bissnes_yandex <= 9),
    bissnes_2gis INTEGER CHECK(bissnes_2gis >= 0 AND bissnes_2gis <= 9),
    bissnes_otzovik INTEGER CHECK(bissnes_otzovik >= 0 AND bissnes_otzovik <= 9)
)
''')

# Add new columns if they don't exist
try:
    cursor.execute("ALTER TABLE companies ADD COLUMN phone TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute("ALTER TABLE companies ADD COLUMN siteurl TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute("ALTER TABLE companies ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

conn.commit()

# Dictionary to keep track of sorting order
sorting_order = {col: False for col in ("ID", "Company Name", "Latitude", "Longitude", "Caption", "Address", "Link", "OGRN", "INN", "OKPO", "Rating", "Yandex", "2GIS", "Otzovik", "Phone", "Site URL", "Email")}

# Function to refresh the Treeview with data from the database
def refresh_treeview():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT place_id, company_name, latitude, longitude, caption, address, link, ogrn, inn, okpo, rating, bissnes_yandex, bissnes_2gis, bissnes_otzovik, phone, siteurl, email FROM companies")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

# Function to sort the Treeview by a specific column
def sort_treeview(col):
    reverse = sorting_order[col]
    sorting_order[col] = not reverse

    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=reverse, key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0])

    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

# Function to save changes to the database
def save_changes(item_id, new_values):
    cursor.execute('''
    UPDATE companies
    SET company_name = ?, latitude = ?, longitude = ?, caption = ?, address = ?, link = ?, ogrn = ?, inn = ?, okpo = ?, rating = ?, bissnes_yandex = ?, bissnes_2gis = ?, bissnes_otzovik = ?, phone = ?, siteurl = ?, email = ?
    WHERE place_id = ?
    ''', (*new_values, item_id))
    conn.commit()
    refresh_treeview()

# Function to open the edit modal window
def open_edit_modal(event):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a company to edit.")
        return

    item_id = tree.item(selected_item, 'values')[0]
    current_values = tree.item(selected_item, 'values')[1:]  # Get current values

    edit_modal = EditModal(root, item_id, current_values, save_changes)

# Set up the main application window
root = tk.Tk()
root.title("Business Data Manager")

# Create a Treeview to display the data
tree = ttk.Treeview(root, columns=("ID", "Company Name", "Latitude", "Longitude", "Caption", "Address", "Link", "OGRN", "INN", "OKPO", "Rating", "Yandex", "2GIS", "Otzovik", "Phone", "Site URL", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Company Name", text="Company Name")
tree.heading("Latitude", text="Latitude")
tree.heading("Longitude", text="Longitude")
tree.heading("Caption", text="Caption")
tree.heading("Address", text="Address")
tree.heading("Link", text="Link")
tree.heading("OGRN", text="OGRN")
tree.heading("INN", text="INN")
tree.heading("OKPO", text="OKPO")
tree.heading("Rating", text="Rating")
tree.heading("Yandex", text="Yandex Rating")
tree.heading("2GIS", text="2GIS Rating")
tree.heading("Otzovik", text="Otzovik Rating")
tree.heading("Phone", text="Phone")
tree.heading("Site URL", text="Site URL")
tree.heading("Email", text="Email")
tree.column("ID", width=50)
tree.column("Company Name", width=150)
tree.column("Latitude", width=100)
tree.column("Longitude", width=100)
tree.column("Caption", width=150)
tree.column("Address", width=200)
tree.column("Link", width=200)
tree.column("OGRN", width=100)
tree.column("INN", width=100)
tree.column("OKPO", width=100)
tree.column("Rating", width=100)
tree.column("Yandex", width=100)
tree.column("2GIS", width=100)
tree.column("Otzovik", width=100)
tree.column("Phone", width=100)
tree.column("Site URL", width=150)
tree.column("Email", width=150)
tree.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

# Bind sorting functionality to column headers
for col in ("ID", "Company Name", "Latitude", "Longitude", "Caption", "Address", "Link", "OGRN", "INN", "OKPO", "Rating", "Yandex", "2GIS", "Otzovik", "Phone", "Site URL", "Email"):
    tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col))

# Bind double-click event to open the edit modal
tree.bind("<Double-1>", open_edit_modal)

# Configure row and column weights for responsiveness
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Load existing data into the Treeview
refresh_treeview()

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
