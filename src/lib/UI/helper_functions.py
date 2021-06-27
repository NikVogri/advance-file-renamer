from tkinter import Tk, HORIZONTAL, OptionMenu, StringVar, Button, Toplevel
from tkinter.messagebox import showerror

from tkinter.ttk import Progressbar
from tkinter import simpledialog

def display_error(title="An error occurred", message="Something went wrong, please try again"):
    root = Tk()
    root.withdraw()
    showerror(title=title, message=message)
    root.destroy()

def get_user_input(heading, prompt):
    user_input = simpledialog.askstring(title=heading, prompt=prompt)
    user_input = user_input.strip()

    if user_input == "":
        return None
    
    return user_input;