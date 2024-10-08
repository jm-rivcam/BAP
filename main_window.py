import tkinter as tk
import psycopg2
import subprocess
import bird_window
from view_registrations import view_registrations
from modify_registrations import modify_registrations
from search_bird import search_bird

def open_registration_window(dbname, sialuq, your_password):
    # This function should open the registration window
    # Assuming bird_window.BirdNameWidget is defined and accepts dbname
    bird_info_window = bird_window.BirdNameWidget(dbname, "sialuq", "your_password")
    bird_info_window.mainloop()

def open_iterm():
    subprocess.run(["open", "-a", "iterm.app"])

def open_main_window(dbname):
    # Create the main window for registrations and actions
    main_window = tk.Tk()
    main_window.geometry("140x230")
    main_window.title('BAP')

    menu = tk.Label(main_window, text="Main menu")
    menu.pack()

    frame = tk.Frame(main_window)
    frame.pack(padx=20, pady=20)

    # Create the buttons and pack them into the frame
    button1 = tk.Button(frame, text="Register", width=50, command=lambda:  open_registration_window(dbname, "sialuq", "your_password"))
    button1.pack(side=tk.TOP)
    
    button2 = tk.Button(frame, text="View", width=50, command=lambda: view_registrations(dbname, "sialuq", "your_password"))
    button2.pack(side=tk.TOP)

    button3 = tk.Button(frame, text="Modify", width=50, command=lambda: modify_registrations(dbname, "sialuq", "your_password"))
    button3.pack(side=tk.TOP)

    button4 = tk.Button(frame, text="Search", width=50, command=lambda: search_bird(dbname, "sialuq", "your_password"))
    button4.pack(side=tk.TOP)

    button5 = tk.Button(frame, text="Recognition", width=50)
    button5.pack(side=tk.TOP)
    
    button6 = tk.Button(frame, text="Open iTerm", command=open_iterm)
    button6.pack(side=tk.TOP)

    main_window.mainloop()

