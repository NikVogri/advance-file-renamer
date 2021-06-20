# -----------------------------------------------------------
# Helper functions
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------

from lib.File import File
from lib.Tmd import Tmd
from lib.Cache import Cache
from lib.Error import Error

import os
import shutil
import tkinter as tk

from lib.config import supported_file_extensions
from lib.UI.helper_functions import display_error

from tkinter.filedialog import askopenfilenames

tmd = Tmd()


def find_episode(episodes, episode_number):
    for episode in episodes:
        if int(episode["episode"]) is int(episode_number):
            return episode
    print("unexpected error: episode not found")


def add_files_to_rename(frame, files):
    """ 
        Opens file selector and adds selected files in memory for future use.
    """
    files.clear()
    added_files = askopenfilenames(initialdir="/", title="Select file / files")

    if len(added_files) > 0:
        for file in added_files:
            _, extension = os.path.splitext(file)

            if extension in supported_file_extensions:
                files.append(File(file))

    render_file_names(frame, files)


def preview_file_names(frame, format_input, files):
    """ 
        Converts file names to selected format & stores the new file name to memory.
    """
    selected_format = format_input.getValue()

    for file in files:
        if "#episodeTitle#" in selected_format and "episodeTitle" not in file.filename_data:
            file_data = file.filename_data
            cached = Cache.read_from_cache(name="temp_cache.txt")

            if cached != -1:
                episode_data = find_episode(cached, file.filename_data["episode"])
                file.filename_data.update(episode_data)
            else:
                episodes = Tmd.fetch_tv_season(title=file_data["title"], season=file_data["season"])
                episode_data = find_episode(episodes, file.filename_data["episode"])
                file.filename_data.update(episode_data)
                # TODO: if no episode is found then ask user to enter title manually

        file.apply_format(selected_format)

    render_file_names(frame, files)


def render_file_names(frame, files_list):
    """ 
        Renders name of each selected file
    """
    for label in frame.winfo_children():
        if isinstance(label, tk.Label):
            label.destroy()

    for file in files_list:
        label = tk.Label(frame, text=f"{file.path.build_path()}\\{file.filename}{file.extension}", width=100)
        label.pack()


def convert_file_names(root, frames, files):
    """ 
        Initiates the renaming of all files stored in memory
    """
    for file in files:
        original_file_full = f'{file.original_path.build_path()}/{file.original_filename}{file.extension}'
        new_full_path = f'{file.path.build_path()}\\{file.filename}{file.extension}'

        if file.path is None or file.original_path.build_path() == file.path.build_path():
            os.rename(original_file_full, new_full_path)
        else:
            if file.path.exists() is False:
                file.path.create()

            if file.path.disk is not file.original_path.disk:
                try:
                    shutil.move(original_file_full, new_full_path)
                except any as error:
                    Error(error).log_to_file()
                    display_error(message="Something went wrong while trying to move files to another disk")
            else:
                os.rename(original_file_full, new_full_path)

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
