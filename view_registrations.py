# view_registrations.py

import tkinter as tk
import psycopg2
from tkinter import ttk
from tkintermapview import TkinterMapView

def view_registrations(dbname, user, password):
    """Opens a window to display bird registrations from the database"""
    view_window = tk.Tk()
    view_window.title("Bird Registrations")

    # Create a canvas for scrolling
    canvas = tk.Canvas(view_window)
    canvas.pack(side="left", fill="both", expand=True)

    # Create a scrollbar for the canvas
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Create a frame to contain all the rows and buttons
    rows_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=rows_frame, anchor="nw")

    # Bind the configure event to update scrollregion
    rows_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

    def open_map_window(latitude, longitude):
        """Opens a new window displaying a map centered on the provided coordinates"""
        map_window = tk.Toplevel()  # Use Toplevel instead of Tk
        map_window.title("Map")

        # Create the map widget
        map_widget = TkinterMapView(map_window, width=400, height=300)
        map_widget.pack(fill="both", expand=True)

        # Set the map center and zoom level
        map_widget.set_position(latitude, longitude)
        map_widget.set_zoom(12)
        map_widget.set_marker(latitude, longitude, text="")

    def on_button_click(coordinates_str):
            
        if "," in coordinates_str:
            lat, long = coordinates_str.split(",")
            lat = float(lat)
            long = float(long)
            # Print latitude and longitude separately
            print(f"Latitude: {lat}")
            print(f"Longitude: {long}")
            open_map_window(lat, long)
        else:
            lat, long = coordinates_str.split(" ")
            lat = float(lat)
            long = float(long)
            # Print latitude and longitude separately
            print(f"Latitude: {lat}")
            print(f"Longitude: {long}")
            open_map_window(lat, long)

    # Create the heading row
    heading_frame = ttk.Frame(rows_frame)
    heading_frame.grid(row=0, column=0, sticky="ew")

    # Define the headings and their respective column widths
    headings = ["Name", "S. Name", "Coordinates", "Action"]
    column_widths = [20, 20, 20, 10]  # Adjust widths as needed

    for idx, (heading, width) in enumerate(zip(headings, column_widths)):
        ttk.Label(heading_frame, text=heading, width=width, anchor="w").grid(row=0, column=idx, padx=5, pady=5, sticky="w")

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

            # Button for the row with coordinates passed as argument
            button = ttk.Button(
                row_frame,
                text="Map",
                command=lambda coordinates_str=coordinates_str: on_button_click(coordinates_str)
            )
            button.grid(row=0, column=3, padx=5, pady=5, sticky="e")

            # Configure column weights to ensure proper stretching
            for col in range(4):
                rows_frame.columnconfigure(col, weight=1)

    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()

    view_window.mainloop()