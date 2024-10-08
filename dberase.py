import tkinter as tk
from tkinter import messagebox
import psycopg2


def delete_database():
  database_name = database_entry.get()

  if not database_name:
    messagebox.showerror("Error", "Please enter a database name.")
  else:
    try:
      # Connect to the PostgreSQL server
      conn = psycopg2.connect(dbname="postgres", user="sialuq", password="your_password")
      conn.autocommit = True  # Enable autocommit
      cursor = conn.cursor()

      # Check if the database exists
      cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = '{database_name}' AND state = 'active';")
      terminations = cursor.rowcount

      # If database is active, terminate connections
      if terminations > 0:
        messagebox.showwarning(
            "Warning",
            f"Database '{database_name}' has active connections. These will be terminated.",
        )

      # Drop the database
      cursor.execute(f"DROP DATABASE {database_name}")

      # Close the connection
      cursor.close()
      conn.close()

      messagebox.showinfo("Success", f"Database '{database_name}' deleted successfully")
    except psycopg2.Error as e:
      if "does not exist" in str(e):
        messagebox.showerror(
            "Error", f"Database '{database_name}' does not exist."
        )
      else:
        messagebox.showerror("Error", f"Error: {e}")


# Create the main window
window = tk.Tk()
window.title("Delete PostgreSQL Database")
window.geometry("350x100")

# Create labels and entry fields
database_label = tk.Label(window, text="Database Name:")
database_label.grid(row=0, column=0, padx=10, pady=10)

database_entry = tk.Entry(window)
database_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to delete the database
delete_button = tk.Button(window, text="Delete Database", command=delete_database)
delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()