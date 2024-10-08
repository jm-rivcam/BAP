import tkinter as tk
from tkinter import messagebox
import psycopg2

def create_database():
    database_name = database_entry.get()

    if not database_name:
        messagebox.showerror("Error", "Please enter a database name.")
    else:
        try:
            # Connect to the PostgreSQL server (replace with your credentials)
            conn = psycopg2.connect(dbname="postgres", user="sialuq", password="your_password")
            conn.autocommit = True  # Enable autocommit
            cursor = conn.cursor()

            # Create the database
            cursor.execute(f"CREATE DATABASE {database_name}")

            # Close the initial connection
            cursor.close()
            conn.close()

            # Connect to the newly created database
            conn = psycopg2.connect(dbname=database_name, user="sialuq", password="your_password")
            cursor = conn.cursor()

            # Create PostGIS extension (if not already installed)
            cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'postgis')")
            exists = cursor.fetchone()[0]
            if not exists:
                cursor.execute("CREATE EXTENSION postgis;")

            # Create the table named 'id'
            cursor.execute("""
                CREATE TABLE id (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    s_name VARCHAR(255),
                    location GEOMETRY(POINT, 4326)
                );
            """)

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Database '{database_name}' created successfully")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

# Create the main window
window = tk.Tk()
window.title("Create PostgreSQL Database")
window.geometry("350x100")

# Create labels and entry fields
database_label = tk.Label(window, text="Database Name:")
database_label.grid(row=0, column=0, padx=10, pady=10)

database_entry = tk.Entry(window)
database_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to create the database
create_button = tk.Button(window, text="Create Database", command=create_database)
create_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()