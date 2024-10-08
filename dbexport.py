import tkinter as tk
from tkinter import filedialog, messagebox
import psycopg2
import csv

def export_database():
    database_name = database_entry.get()

    if not database_name:
        messagebox.showerror("Error", "Please enter a database name.")
        return

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=database_name, user="sialuq", password="your_password")
        cursor = conn.cursor()

        # Check if the 'id' table exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='id');")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            messagebox.showerror("Error", "Table 'id' does not exist in the database.")
            return

        # Create a file dialog to choose the export location
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=database_name + ".csv")

        if file_path:
            # Prepare the SQL query to extract the data
            cursor.execute(f"""
                SELECT name, s_name, ST_Y(location) AS latitude, ST_X(location) AS longitude
                FROM id;
            """)
            data = cursor.fetchall()

            # Get column names
            column_names = ['Name', 'Scientific Name', 'Latitude', 'Longitude']

            # Open the CSV file
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                # Write header row
                writer.writerow(column_names)

                # Write data rows
                writer.writerows(data)

            messagebox.showinfo("Success", f"Data from table 'id' exported successfully.")

        # Close the connection
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create the main window
window = tk.Tk()
window.title("Export PostgreSQL Database")
window.geometry("350x100")

# Create labels and entry fields
database_label = tk.Label(window, text="Database Name:")
database_label.grid(row=0, column=0, padx=10, pady=10)

database_entry = tk.Entry(window)
database_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to export the database
export_button = tk.Button(window, text="Export Database", command=export_database)
export_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()