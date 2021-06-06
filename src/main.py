import tkinter as tk

import requests

from tkinter import *
from tkinter.filedialog import askopenfilenames

from lib.File import File

from lib.UI.Text import Text

file = File()

# config = {
#     ["movie_format"]: ("TITLE", "YYYY_DATE"),
#     ["tv_format"]: {
#         ["show"]: ("TITLE", "SEASON"),
#         ["episode"]: ("EPISODE_TITLE", "SEASON", "SEASON_NUMBER", "EPISODE", "EPISODE_NUMBER")
#     }
# }

# default = "Game of Thrones/Season 1/Game of Thrones - 1x1 - Winter is coming"


def add_files_to_rename():
    files = askopenfilenames(initialdir="/", title="Select file / files")

    if (len(files) > 0):
        file.addFiles(files)
    else:
        file.removeFiles()

    file.renderFilenames(selector_frame)


def change_filenames():
    print("hello")


def find_original(text):
    print(text)


def convert_files():
    title = title_input.getValue()
    season = season_input.getValue("number")
    selected_format = format_input.getValue()

    print(title, season, selected_format)
    # api_key = ""
    # url = f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&page=1&query={title}&include_adult=false'

    # response = requests.get(url)
    # response = response.json()

    # if (len(response["results"]) > 1):
    #     pass

    # show_id = response["id"]

    # requests.get()


root = Tk()
root.title("Renamer")
root.resizable(False, False)

canvas = tk.Canvas(root, height=700, width=600)
canvas.pack()


selector_frame = tk.Frame(
    root, bg="#fefefe", highlightbackground="#f0f0f0", highlightthickness=0.5)
selector_frame.place(relwidth=0.5, relheight=0.75)

result_frame = tk.Frame(
    root, bg="#fefefe", highlightbackground="#f0f0f0", highlightthickness=0.5)
result_frame.place(relwidth=0.5, relheight=0.75, relx=0.5)

upload_button = tk.Button(
    selector_frame, text="Select", command=add_files_to_rename)
upload_button.pack(side=tk.BOTTOM)

configuration_frame = tk.Frame(
    root, highlightbackground="#f0f0f0", highlightthickness=0.5, bg="#fefefe")
configuration_frame.place(relwidth=1, relheight=0.25, rely=0.75)


configuration_frame_labels = tk.Frame(
    configuration_frame, width=200, height=173).place(x=0)
configuration_frame_inputs = tk.Frame(
    configuration_frame, width=200, height=173).place(x=200)
configuration_frame_actions = tk.Frame(
    configuration_frame, width=200, height=173).place(x=400)

title_label = tk.Label(configuration_frame_labels, text="Title: ").place(x=10, y=550)
format_label = tk.Label(configuration_frame_labels, text="Format: ").place(x=10, y=570)
season_label = tk.Label(configuration_frame_labels, text="Season: ").place(x=10, y=590)

title_input = Text(configuration_frame_labels).position(x=70, y=550)
format_input = Text(configuration_frame_labels).position(x=70, y=570)
season_input = Text(configuration_frame_labels).position(x=70, y=590)


# tk.Label(configuration_frame_labels, text="Title #t#, Season number #sn#, Episode number #en#, Year #y#").place(x=10, y=590)
tk.Button(configuration_frame_labels, text="Convert now", height=8,
          width=11, command=convert_files).place(x=510, y=550)

if (__name__ == "__main__"):
    root.mainloop()
