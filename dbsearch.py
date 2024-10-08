import tkinter as tk
from tkinter import messagebox
import psycopg2


def update_database_list():
    # Clear the current list
    database_listbox.delete(0, tk.END)

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(dbname="postgres", user="sialuq", password="your_password")
        cursor = conn.cursor()

        # Retrieve the list of databases
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()

        # Insert database names into the listbox
        for db in databases:
            database_listbox.insert(tk.END, db[0])

        # Close the connection
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error retrieving databases: {e}")


# Create the main window
window = tk.Tk()
window.title("List PostgreSQL Databases")
window.geometry("472x200")

# Create a label for the list
title_label = tk.Label(window, text="Databases:")
title_label.grid(row=0, column=0, padx=10, pady=10)

# Create a listbox to display databases
database_listbox = tk.Listbox(window, height=15, width=50)
database_listbox.grid(row=1, column=0, padx=10, pady=10)

# Fetch and display the database list when the application starts
update_database_list()

# Start the Tkinter event loop
window.mainloop()