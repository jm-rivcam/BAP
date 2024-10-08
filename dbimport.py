import tkinter as tk
from tkinter import filedialog, messagebox
import psycopg2
import csv

def import_database():
    database_name = database_entry.get()

    if not database_name:
        messagebox.showerror("Error", "Please enter a database name.")
        return

    # Ask the user for the CSV file to import
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if not file_path:
        return  # User canceled the file dialog

    try:
        conn = psycopg2.connect(dbname=database_name, user="sialuq", password="your_password")
        cursor = conn.cursor()

        # Open the CSV file
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile)

            # Skip the header row
            next(reader)

            for row in reader:
                if len(row) != 4:
                    messagebox.showwarning("Warning", "Row does not have exactly 4 columns, skipping.")
                    continue  # Skip rows that do not have 4 columns

                name, scientific_name, latitude, longitude = row

                try:
                    # Convert latitude and longitude to floats
                    latitude = float(latitude.strip())
                    longitude = float(longitude.strip())
                except ValueError:
                    messagebox.showwarning("Warning", f"Invalid latitude or longitude: {latitude}, {longitude}. Skipping row.")
                    continue

                # Create the geometry string
                location = f'POINT({longitude} {latitude})'

                sql = """
                    INSERT INTO id (name, s_name, location)
                    VALUES (%s, %s, ST_GeomFromText(%s, 4326))
                """
                cursor.execute(sql, (name, scientific_name, location))

        conn.commit()
        messagebox.showinfo("Success", "Data imported successfully.")

    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Create the main window for importing
window = tk.Tk()
window.title("Import PostgreSQL Database")
window.geometry("350x100")

# Create labels and entry fields
database_label = tk.Label(window, text="Database Name:")
database_label.grid(row=0, column=0, padx=10, pady=10)

database_entry = tk.Entry(window)
database_entry.grid(row=0, column=1, padx=10, pady=10)

# Create an import button
import_button = tk.Button(window, text="Import Database", command=import_database)
import_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()