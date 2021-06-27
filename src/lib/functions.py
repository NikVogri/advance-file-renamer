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

from tkinter.filedialog import askopenfilenames, askdirectory
from lib.UI.helper_functions import get_user_input

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


def search_dir_files(frame, files):
    """ 
        Opens directory selector & appends files inside of a dir
    """
    directory_path = askdirectory()
    if directory_path == "":
        return

    files.clear()
    # dir_files = os.listdir(directory_path)

    dir_files = []
    for (dirpath, dirnames, filenames) in os.walk(directory_path):
        dir_files += [os.path.join(dirpath, file) for file in filenames]

    if len(dir_files) > 0:
        for file in dir_files:
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
            cached = Cache.read_from_cache(name="main.txt")

            if cached != -1 and file_data["season"] in cached:
                episode_data = find_episode(cached[file_data["season"]], file.filename_data["episode"])
                file.filename_data.update(episode_data)
            else:
                if not file_data["title"]:
                    title = get_user_input(heading="Found no matches", prompt="Enter tv show title (example: Game of thrones)")
                else:
                    title = file_data["title"]
                
                tv_shows = Tmd.fetch_tv_show(title=title)

                if tv_shows is None or len(tv_shows) < 1:
                    while True:
                        title = get_user_input(heading="Found no matches", prompt="Enter tv show title (example: Game of thrones)")
                        tv_shows = Tmd.fetch_tv_show(title=title)
                        if tv_shows != None and len(tv_shows) > 0:
                            break

                if len(tv_shows) > 1:
                    print("MORE THAN ONE FOUND, SELECTING THE FIRST ITEM")
                    # TODO: let user decide which one is correct

                episodes = Tmd.fetch_season(tv_shows[0], file_data["season"], cache=True)
                episode_data = find_episode(episodes, file.filename_data["episode"])
                file.filename_data.update(episode_data)

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
        label = tk.Label(frame, text=f"{file.path.build_path()}{os.path.sep}{file.filename}{file.extension}", width=100)
        label.pack()


def convert_file_names(root, frames, files):
    """ 
        Initiates the renaming of all files stored in memory
    """
    for file in files:
        original_file_full = f'{file.original_path.build_path()}{os.path.sep}{file.original_filename}{file.extension}'
        new_full_path = f'{file.path.build_path()}{os.path.sep}{file.filename}{file.extension}'

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


def handle_graceful_close(root):
    Cache.clear_file_from_cache("main.txt")
    root.destroy()