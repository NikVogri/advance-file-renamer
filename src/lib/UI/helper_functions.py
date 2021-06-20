from tkinter import Tk, HORIZONTAL
from tkinter.messagebox import showerror
from tkinter.ttk import Progressbar

def display_error(title="An error occurred", message="Something went wrong, please try again"):
    root = Tk()
    root.withdraw()
    showerror(title=title, message=message)
    root.destroy()
