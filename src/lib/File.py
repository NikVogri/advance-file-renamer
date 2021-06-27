# -----------------------------------------------------------
# File class wrapper
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import PTN
import os
import re

from lib.FilePath import FilePath


class File():
    def __init__(self, original_file_path):
        self.original_file_path = original_file_path
        path, extension = os.path.splitext(self.original_file_path)

        path = path.replace("/", os.path.sep)
        path = path.replace("//", os.path.sep)
        path = path.replace("\\", os.path.sep)

        seperated_path = path.split(os.path.sep)

        self.extension = extension

        self.original_path = FilePath(path)
        self.path = FilePath(path)

        self.original_filename = seperated_path[-1]
        self.filename = seperated_path[-1]

        self.filename_data = self.parse_filename()
        self.content_type = "tv" if "season" in self.filename_data else "movie"

    def parse_filename(self):
        """ 
            Extracts data from filename
        """
        filename_data = PTN.parse(self.filename)
        for key, val in filename_data.items():
            if isinstance(val, int):
                val = str(val)
                filename_data[key] = str(val)
            if isinstance(val, str):
                filename_data[key] = val.replace(".", "").replace("#", "")
        return filename_data

    def apply_format(self, selected_format):
        """ 
            Applies format to file path and filename
        """
        path, extension = os.path.splitext(selected_format)

        path = path.replace("/", os.path.sep)
        path = path.replace("//", os.path.sep)
        path = path.replace("\\", os.path.sep)

        seperated_path = path.split(os.path.sep)
        filename = seperated_path[-1]

        if self.filename == selected_format or selected_format == "":
            return

        self.filename = self.map_str_to_values(filename)
        self.path = FilePath(self.map_str_to_values(path))

    def map_str_to_values(self, map_string):
        matches = re.finditer(r"#[A-Za-z0-9]*#", map_string)

        for match in matches:
            to_replace = match.group()
            key = to_replace.replace("#", "")

            if key not in self.filename_data:
                continue

            map_string = map_string.replace(to_replace, f"{self.filename_data[key]}")

        return map_string
