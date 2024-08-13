import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class AirlineSystem:
    def __init__(self, root):
        self.root = root
        self.root.title('Airline System')
        self.root.geometry("1920x1080")
        self.root.state('zoomed')  # Make the window full screen

        # Create frames
        self.frame_image = tk.Frame(self.root, bg='gray')
        self.frame_image.pack(fill='x')

        self.frame_flights = tk.Frame(self.root, bg='gray')
        self.frame_flights.pack(fill='both', expand=True)

        self.frame_book = tk.Frame(self.root, bg='gray')
        self.frame_book.pack(fill='x')

        # Add image to the top frame
        pil_image = Image.open('gg.png')
        pil_image = pil_image.resize((1960, 500))
        self.image = ImageTk.PhotoImage(pil_image)
        self.label_image = tk.Label(self.frame_image, image=self.image)
        self.label_image.pack()

        # Create flight list treeview
        self.tree_flights = ttk.Treeview(self.frame_flights, columns=('flight_number', 'origin', 'destination', 'departure_date', 'return_date', 'price'))
        self.tree_flights.pack(fill='both', expand=True)
        self.tree_flights.heading('#0', text='ID')
        self.tree_flights.heading('#1', text='Flight Number')
        self.tree_flights.heading('#2', text='Origin')
        self.tree_flights.heading('#3', text='Destination')
        self.tree_flights.heading('#4', text='Departure Date')
        self.tree_flights.heading('#5', text='Return Date')
        self.tree_flights.heading('#6', text='Price')

        # Create book flight frame
        tk.Label(self.frame_book, text='Book Flight').pack()
        self.entry_flight_number = tk.Entry(self.frame_book)
        self.entry_flight_number.pack()
        self.button_book = tk.Button(self.frame_book, text='Book', command=self.book_flight)
        self.button_book.pack()

        # Connect to the database
        self.conn = sqlite3.connect('flights.db')
        self.c = self.conn.cursor()

        # Create table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS flights
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, flight_number TEXT, origin TEXT, destination TEXT, departure_date TEXT, return_date TEXT, price REAL)''')
        self.conn.commit()

        # Load flights from database
        self.load_flights()

    def load_flights(self):
        self.tree_flights.delete(*self.tree_flights.get_children())
        self.c.execute('SELECT * FROM flights')
        flights = self.c.fetchall()
        for flight in flights:
            self.tree_flights.insert('', 'end', values=flight)

    def book_flight(self):
        flight_number = self.entry_flight_number.get()
        self.c.execute('SELECT * FROM flights WHERE flight_number=?', (flight_number,))
        flight = self.c.fetchone()
        if flight:
            # Book the flight (insert into bookings table, etc.)
            messagebox.showinfo('Flight Booked', f'Flight {flight_number} has been booked!')
            self.entry_flight_number.delete(0, tk.END)  # Clear the entry field
        else:
            messagebox.showerror('Flight Not Found', f'Flight {flight_number} not found.')

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

root = tk.Tk()
app = AirlineSystem(root)
root.mainloop()
