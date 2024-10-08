import tkinter as tk
import psycopg2
import subprocess
import bird_window
from tkinter import ttk

def search_bird(dbname, user, password):
    """Opens a window to search for birds by name or scientific name."""
    search_window = tk.Toplevel()  # Use Toplevel to create a new window
    search_window.title("Search Bird")
    search_window.geometry("400x200")
    search_window.resizable(True, True)

    # Create a frame for the search entry
    search_frame = ttk.Frame(search_window)
    search_frame.pack(padx=10, pady=10)

    # Entry for the search term
    ttk.Label(search_frame, text="Enter name or scientific name:").grid(row=0, column=0, padx=5, pady=5)
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create a canvas for displaying search results
    result_canvas = tk.Canvas(search_window)
    result_canvas.pack(side="left", fill="both", expand=True)

    # Create a scrollbar for the canvas
    result_scrollbar = ttk.Scrollbar(search_window, orient="vertical", command=result_canvas.yview)
    result_scrollbar.pack(side="right", fill="y")
    result_canvas.configure(yscrollcommand=result_scrollbar.set)

    # Frame to contain the results
    results_frame = ttk.Frame(result_canvas)
    result_canvas.create_window((0, 0), window=results_frame, anchor="nw")

    # Bind the configure event to update scrollregion
    results_frame.bind("<Configure>", lambda e: result_canvas.config(scrollregion=result_canvas.bbox("all")))

    def perform_search():
        """Performs the search in the database."""
        search_term = search_entry.get()
        
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        # Connect to the database and search for birds
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password)
            cur = conn.cursor()

            # Search query
            sql = """
                SELECT name, s_name, ST_AsText(location) AS location_text 
                FROM id 
                WHERE name ILIKE %s OR s_name ILIKE %s;
            """
            cur.execute(sql, (f"%{search_term}%", f"%{search_term}%"))

            rows = cur.fetchall()

            for row_index, row in enumerate(rows):
                location_text = row[2]  # Get the location text
                coordinates_str = location_text.split("(")[1].split(")")[0]  # Extract coordinates

                row_frame = ttk.Frame(results_frame)
                row_frame.grid(row=row_index, column=0, sticky="ew")

                # Labels for each column
                ttk.Label(row_frame, text=row[0], width=20, anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                ttk.Label(row_frame, text=row[1], width=20, anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky="w")
                ttk.Label(row_frame, text=coordinates_str, width=20, anchor="w").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            if conn:
                cur.close()
                conn.close()

    # Button to perform the search
    search_button = ttk.Button(search_frame, text="Search", command=perform_search)
    search_button.grid(row=1, column=1, padx=5, pady=5)