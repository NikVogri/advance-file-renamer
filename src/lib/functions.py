# -----------------------------------------------------------
# Helper functions
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------

from lib.File import File
from lib.Tmd import Tmd
from lib.Cache import Cache
from lib.FilePath import FilePath

import re
import tkinter as tk

from tkinter.filedialog import askopenfilenames

tmd = Tmd()


def add_files_to_rename(frame, files):
    """ 
        Opens file selector and adds selected files in memory for future use.
    """
    added_files = askopenfilenames(initialdir="/", title="Select file / files")

    files.clear()
    if len(added_files) > 0:
        for file in added_files:
            files.append(File(file))

    render_file_names(frame, files)


def preview_file_names(frame, format_input, files):
    """ 
        Converts file names to selected format & stores the new file name to memory.
    """
    selected_format = format_input.getValue()

    for file in files:
        file.apply_format(selected_format)

    render_file_names(frame, files)


def render_file_names(frame, files_list):
    """ 
        Renders name of each file stored in memory
    """
    for label in frame.winfo_children():
        if isinstance(label, tk.Label):
            label.destroy()

    for file in files_list:
        label = tk.Label(frame, text=file.filename, width=100)
        label.pack()


def convert_file_names(frames, files, selected_format):
    """ 
        Initiates the renaming of all files stored in memory
    """
    for file in files:
        if re.compile("[A-Z]:/").search(selected_format):
            file.rename(new_path=FilePath(selected_format))
        else:
            file.rename(new_path=None)
    files.clear()

    for frame in frames:
        render_file_names(frame, files)
    
    cache = Cache()
    cache.clear_file_from_cache()


def save_format(format_string):
    """ 
        Saves format input to file
    """
    selected_format = format_string.getValue()

    if selected_format.strip() != "":
        cache = Cache()
        cache.add_to_cache(selected_format, name="format.txt")
