import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import subprocess
from PIL import Image, ImageTk

# Create a database connection
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Create a table to store flight information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT,
        departure_airport TEXT,
        arrival_airport TEXT,
        departure_date DATE,
        class TEXT,
        passengers INTEGER
    )
''')

# Function to save flight information to the database
def save_flight():
    flight_number = flight_number_entry.get()
    departure_airport = departure_airport_entry.get()
    arrival_airport = arrival_airport_entry.get()
    departure_date = departure_date_entry.get()
    flight_class = class_entry.get()
    passengers = passengers_entry.get()
    
    # Handle empty fields
    if not flight_number or not departure_airport or not arrival_airport or not departure_date or not flight_class or not passengers:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        passengers = int(passengers)
    except ValueError:
        messagebox.showerror("Error", "Passengers must be an integer")
        return

    # Validate date format
    try:
        datetime.datetime.strptime(departure_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        return

    # Insert the data into the database
    cursor.execute('''
        INSERT INTO flights (flight_number, departure_airport, arrival_airport, departure_date, class, passengers)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (flight_number, departure_airport, arrival_airport, departure_date, flight_class, passengers))
    conn.commit()

    # Clear the input fields
    flight_number_entry.delete(0, tk.END)
    departure_airport_entry.delete(0, tk.END)
    arrival_airport_entry.delete(0, tk.END)
    departure_date_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    passengers_entry.delete(0, tk.END)
    
    # Show a confirmation message
    messagebox.showinfo("Success", "Flight information saved successfully")

# Function to open the invo.py file
def open_booking_page():
    root.destroy()
    import invo

# Create the main window
root = tk.Tk()
root.title("Add Flight")

# Create labels and entry fields for flight information
flight_number_label = ttk.Label(root, text="Flight Number:")
flight_number_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
flight_number_entry = ttk.Entry(root)
flight_number_entry.grid(row=0, column=1, padx=5, pady=5)

departure_airport_label = ttk.Label(root, text="Departure Airport:")
departure_airport_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
departure_airport_entry = ttk.Entry(root)
departure_airport_entry.grid(row=1, column=1, padx=5, pady=5)

arrival_airport_label = ttk.Label(root, text="Arrival Airport:")
arrival_airport_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
arrival_airport_entry = ttk.Entry(root)
arrival_airport_entry.grid(row=2, column=1, padx=5, pady=5)

departure_date_label = ttk.Label(root, text="Departure Date (YYYY-MM-DD):")
departure_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
departure_date_entry = ttk.Entry(root)
departure_date_entry.grid(row=3, column=1, padx=5, pady=5)

class_label = ttk.Label(root, text="Class:")
class_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
class_entry = ttk.Entry(root)
class_entry.grid(row=4, column=1, padx=5, pady=5)

passengers_label = ttk.Label(root, text="Number of Passengers:")
passengers_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
passengers_entry = ttk.Entry(root)
passengers_entry.grid(row=5, column=1, padx=5, pady=5)

# Create a button to save the flight information
save_button = ttk.Button(root, text="Save Flight", command=save_flight)
save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create a button to open the booking page
book_flight_button = ttk.Button(root, text="Go to Book Flights", command=open_booking_page)
book_flight_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Run the main event loop
root.mainloop()

# Close the database connection
conn.close()
