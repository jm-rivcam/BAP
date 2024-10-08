import tkinter as tk
import subprocess
from main_window import open_main_window  # Import the function from the second file

# Global variable for the database name
dbname = ""

def create_icon_window():
    # Create the main window
    window = tk.Tk()
    window.title("Menu")
    window.resizable(False, False)
    window.geometry("550x90")

    # Load the images (replace with your actual image paths)
    image_paths = ["icons/add.png", "icons/del.png", "icons/search.png",
                   "icons/work.png", "icons/import.png", "icons/export.png"]
    labels = ["Add", "Delete", "Search", "Work", "Import", "Export"]

    images = []

    for i in range(len(image_paths)):
        frame = tk.Frame(window)
        frame.pack(side="left", padx=5)

        icon_image = tk.PhotoImage(file=image_paths[i])
        images.append(icon_image)

        button = tk.Button(frame, image=icon_image, command=lambda i=i: button_action(i))
        button.pack()

        label = tk.Label(frame, text=labels[i], bg=window.cget("bg"))
        label.pack()

    window.mainloop()

def button_action(button_index):
    # Call the appropriate function based on the button index
    if button_index == 0:
        add_function()
    elif button_index == 1:
        delete_function()
    elif button_index == 2:
        search_function()
    elif button_index == 3:
        get_dbname_window()  # "Work" button clicked
    elif button_index == 4:
        import_function()
    elif button_index == 5:
        export_function()

def add_function():
    subprocess.run(["python", "dbregister.py"]) 
    # Implement add functionality here

def delete_function():
    subprocess.run(["python", "dberase.py"]) 
    # Implement delete functionality here

def search_function():
    subprocess.run(["python", "dbsearch.py"]) 
    # Implement search functionality here

def import_function():
    subprocess.run(["python", "dbimport.py"]) 
    # Implement import functionality here

def export_function():
    subprocess.run(["python", "dbexport.py"]) 
    # Implement export functionality here

def get_dbname_window():
    dbname_window = tk.Toplevel()
    dbname_window.title("Enter Database Name")
    dbname_window.resizable(False, False)

    label = tk.Label(dbname_window, text="Enter Database Name:")
    label.pack()

    entry = tk.Entry(dbname_window)
    entry.pack()

    def get_and_close():
        global dbname
        dbname = entry.get()
        dbname_window.destroy()
        open_main_window(dbname)  # Pass the dbname to the second window

    submit_button = tk.Button(dbname_window, text="Submit", command=get_and_close)
    submit_button.pack()

if __name__ == "__main__":
    create_icon_window()