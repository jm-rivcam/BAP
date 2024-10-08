import tkinter as tk
import psycopg2
import subprocess
import bird_window
from view_registrations import view_registrations
from tkinter import ttk

def modify_registrations(dbname, user, password):
    """Opens a window to modify bird registrations from the database"""
    modify_window = tk.Tk()
    modify_window.title("Modify Registrations")

    # Create a canvas for scrolling
    canvas = tk.Canvas(modify_window)
    canvas.pack(side="left", fill="both", expand=True)

    # Create a scrollbar for the canvas
    scrollbar = ttk.Scrollbar(modify_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Create a frame to contain all the rows and buttons
    rows_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=rows_frame, anchor="nw")

    # Bind the configure event to update scrollregion
    rows_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

    # Create the heading row
    heading_frame = ttk.Frame(rows_frame)
    heading_frame.grid(row=0, column=0, sticky="ew")

    # Define the headings and their respective column widths
    headings = ["Name", "S. Name", "Coordinates", "Action"]
    column_widths = [20, 20, 20, 10]

    for idx, (heading, width) in enumerate(zip(headings, column_widths)):
        ttk.Label(heading_frame, text=heading, width=width, anchor="w").grid(row=0, column=idx, padx=5, pady=5, sticky="w")

    def edit_registration(name, scientific_name, coordinates_str):
        """Opens a window to edit the selected registration."""
        edit_window = tk.Toplevel(modify_window)
        edit_window.title("Edit Registration")

        # Create labels and entry fields
        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, name)

        ttk.Label(edit_window, text="Scientific Name:").grid(row=1, column=0, padx=5, pady=5)
        scientific_name_entry = ttk.Entry(edit_window)
        scientific_name_entry.grid(row=1, column=1, padx=5, pady=5)
        scientific_name_entry.insert(0, scientific_name)

        ttk.Label(edit_window, text="Coordinates (Lat, Long):").grid(row=2, column=0, padx=5, pady=5)
        coordinates_entry = ttk.Entry(edit_window)
        coordinates_entry.grid(row=2, column=1, padx=5, pady=5)
        coordinates_entry.insert(0, coordinates_str)

        def save_changes():
            new_name = name_entry.get()
            new_scientific_name = scientific_name_entry.get()
            new_coordinates = coordinates_entry.get()

            # Update the database
            try:
                conn = psycopg2.connect(dbname=dbname, user=user, password=password)
                cur = conn.cursor()

                # Update the entry in the database
                sql = """
                      UPDATE id 
                      SET name = %s, s_name = %s, location = ST_GeomFromText(%s, 4326) 
                      WHERE name = %s AND s_name = %s;
                      """
                cur.execute(sql, (new_name, new_scientific_name, f"POINT({new_coordinates})", name, scientific_name))

                conn.commit()
                print("Registration updated successfully!")

                # Close the edit window
                edit_window.destroy()

            except psycopg2.Error as e:
                print("Error:", e)
            finally:
                if conn:
                    cur.close()
                    conn.close()

        # Buttons to save or cancel
        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=3, column=0, padx=5, pady=5)
        cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.grid(row=3, column=1, padx=5, pady=5)

    # Connect to the database and retrieve bird registrations
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)
        cur = conn.cursor()

        # Select all columns (including location)
        sql = "SELECT name, s_name, ST_AsText(location) AS location_text FROM id;"
        cur.execute(sql)

        rows = cur.fetchall()

        for row_index, row in enumerate(rows):
            location_text = row[2]  # Get the location text
            coordinates_str = location_text.split("(")[1].split(")")[0]  # Extract coordinates

            row_frame = ttk.Frame(rows_frame)
            row_frame.grid(row=row_index + 1, column=0, sticky="ew")

            # Labels for each column
            ttk.Label(row_frame, text=row[0], width=20, anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(row_frame, text=row[1], width=20, anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky="w")
            ttk.Label(row_frame, text=coordinates_str, width=20, anchor="w").grid(row=0, column=2, padx=5, pady=5, sticky="w")


            # Button for editing registration
            edit_button = ttk.Button(
                row_frame,
                text="Edit",
                command=lambda name=row[0], scientific_name=row[1], coordinates_str=coordinates_str: edit_registration(name, scientific_name, coordinates_str)
            )
            edit_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

            # Configure column weights to ensure proper stretching
            for col in range(5):
                rows_frame.columnconfigure(col, weight=1)

    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()

    modify_window.mainloop()