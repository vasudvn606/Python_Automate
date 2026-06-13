import tkinter as tk
from tkinter import messagebox

# Create a hidden root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Show the message box
messagebox.showinfo("Message", "Hi")

# Destroy the root window after the message box is closed
root.destroy()
