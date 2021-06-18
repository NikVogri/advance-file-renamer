# -----------------------------------------------------------
# Render initial application using tkinter
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------

from tkinter import *
from lib.functions import *
from lib.UI.Text import Text

root = Tk()
root.title("Advance Movie & TV Show renamer")
root.resizable(False, False)


def render_ui():
    files = []

    canvas = tk.Canvas(root, height=700, width=1200)
    canvas.pack()

    selector_frame = tk.Frame(
        root, bg="#fefefe", highlightbackground="#f0f0f0", highlightthickness=0.5)

    selector_frame.place(relwidth=0.5, relheight=0.75)

    result_frame = tk.Frame(
        root, bg="#fefefe", highlightbackground="#f0f0f0", highlightthickness=0.5)
    result_frame.place(relwidth=0.5, relheight=0.75, relx=0.5)

    upload_button = tk.Button(
        selector_frame, text="Select", command=lambda: add_files_to_rename(selector_frame, files))
    upload_button.pack(side=tk.BOTTOM)

    configuration_frame = tk.Frame(
        root, highlightbackground="#f0f0f0", highlightthickness=0.5, bg="#fefefe")
    configuration_frame.place(relwidth=1, relheight=0.25, rely=1)

    configuration_frame_labels = tk.Frame(
        configuration_frame, width=400, height=173).place(x=0)
    configuration_frame_inputs = tk.Frame(
        configuration_frame, width=600, height=173).place(x=200)
    configuration_frame_actions = tk.Frame(
        configuration_frame, width=400, height=173).place(x=400)

    format_label = tk.Label(configuration_frame_labels,
                            text="Desired format: ").place(x=10, y=570)

    format_label2 = tk.Label(configuration_frame_labels,
                             text="title - #title# \n year - #year# \n season - #season \n episode - #episode# \n episodeTitle - #episodeTitle#").place(
        x=700, y=570)

    format_input = Text(configuration_frame_labels,
                        width=100).position(x=10, y=590)

    tk.Button(configuration_frame_labels, text="Preview", height=3,
              width=11, command=lambda: preview_file_names(result_frame, format_input, files)).place(x=1100, y=550)

    tk.Button(configuration_frame_labels, text="Rename", height=3, width=11,
              command=lambda: convert_file_names([selector_frame, result_frame], files, format_input.getValue())).place(
        x=1100, y=620)

    tk.Button(configuration_frame_labels, text="Save format", height=1,
              width=10, command=lambda: save_format(format_input)).place(x=10, y=615)

    format_input.set_cached_value()
    root.mainloop()
