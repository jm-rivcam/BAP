import tkinter as tk
import psycopg2

# Database connection details (replace with your actual values)

class BirdNameWidget(tk.Tk):
        def __init__(self, dbname, username, password):
            super().__init__()
            self.title("Bird Information Entry")
            
            # Store database details
            self.dbname = dbname
            self.username = username
            self.password = password

            # Create a frame to hold all widgets
            self.main_frame = tk.Frame(self)
            self.main_frame.pack(padx=10, pady=10)

            # Labels and entry fields (using grid layout for side-by-side placement)
            self.name_label = tk.Label(self.main_frame, text="Name:")
            self.name_label.grid(row=0, column=0, sticky="W")

            self.name_entry = tk.Entry(self.main_frame)
            self.name_entry.grid(row=0, column=1, padx=5)

            self.scientific_name_label = tk.Label(self.main_frame, text="Scientific Name:")
            self.scientific_name_label.grid(row=1, column=0, sticky="W")

            self.scientific_name_entry = tk.Entry(self.main_frame)
            self.scientific_name_entry.grid(row=1, column=1, padx=5)

            self.location_label = tk.Label(self.main_frame, text="Location (Lat, Long):")
            self.location_label.grid(row=2, column=0, sticky="W")

            self.location_entry = tk.Entry(self.main_frame)
            self.location_entry.grid(row=2, column=1, padx=5)

            # Create save button (grid for more control over placement)
            self.save_button = tk.Button(self.main_frame, text="Save", command=self.save_info)
            self.save_button.grid(row=3, column=0, pady=10)  # Place in row 3, column 0

            # Create exit button (grid for more control over placement)
            self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.quit)
            self.exit_button.grid(row=3, column=1, pady=10)  # Place in row 3, column 1


        def save_info(self):
            name = self.name_entry.get()
            scientific_name = self.scientific_name_entry.get()
            location_text = self.location_entry.get()

            # Assuming location is entered as comma-separated lat, long
            try:
                longitude, latitude = location_text.split(",")
                longitude = float(longitude.strip())
                latitude = float(latitude.strip())
                location = f"POINT({longitude} {latitude})"  # Format for ST_GeomFromText
            except ValueError:
                print("Error: Location must be in the format 'latitude,longitude'.")
                return  # Exit the function if location is not in the correct format

            if name and scientific_name and location:
                try:
                    # Connect to the database using instance variables
                    conn = psycopg2.connect(dbname=self.dbname, user=self.username, password=self.password)
                    cur = conn.cursor()

                    # Insert the data into the table
                    sql = """
                          INSERT INTO id (name, s_name, location)
                          VALUES (%s, %s, ST_GeomFromText(%s, 4326))
                          """
                    cur.execute(sql, (name, scientific_name, location))

                    # Commit the changes
                    conn.commit()

                    print("Bird information inserted successfully!")

                except psycopg2.Error as e:
                    print("Error:", e)
                finally:
                    # Close the cursor and connection
                    cur.close()
                    conn.close()