# -----------------------------------------------------------
# File class wrapper
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import tkinter as tk
import PTN
import os
from lib.Tmd import Tmd
from lib.Cache import Cache
class File(Tmd, Cache):
    def __init__(self, original_file_path):
        self.original_file_path = original_file_path
        self.parse_file()

    def parse_file(self):
        """ 
            Breaks file path & name into pieces for future use
        """
        path, extension = os.path.splitext(self.original_file_path)

        seperated_path = path.split('/')

        self.extension = extension
        self.disk = seperated_path[0]
        self.directories = seperated_path[1:-1]
        self.filename = seperated_path[-1]
        self.file_data = self.parse_filename()
        self.content_type = "tv" if "season" in self.file_data else "movie"

    def parse_filename(self):
        """ 
            Extracts data from filename
        """
        parsed_filename = PTN.parse(self.filename)

        for key, val in parsed_filename.items():

            if (isinstance(val, int)):
                val = str(val)
                parsed_filename[key] = str(val)

            if "." in val:
                parsed_filename[key] = val.replace(".", "")
            if "#" in val:
                parsed_filename[key] = val.replace("#", "")
            if "!" in val:
                parsed_filename[key] = val.replace("!", "")
            if "@" in val:
                parsed_filename[key] = val.replace("@", "")

        return parsed_filename

    def apply_format(self, selected_format):
        """ 
            Applies format to filename
        """
        if self.filename == selected_format or selected_format == "":
            return
        new_filename = selected_format

        if self.content_type == "movie":
            if "#title#" in selected_format:
                new_filename = new_filename.replace(
                    "#title#", self.file_data["title"])

            if "#year#" in selected_format:
                new_filename = new_filename.replace(
                    "#year#", self.file_data["year"])

        if self.content_type == "tv":
            if "#episodeTitle#" in selected_format:
                if "episodeName" in self.file_data:
                    new_filename = new_filename.replace(
                        "#episodeTitle#", self.file_data["episodeName"])
                else:
                    file_data = self.file_data
                    cached = self.read_from_cache()
                    if cached != -1:
                        print(cached)
                        episode_data = self.find_correct_episode(cached)
                        new_filename = new_filename.replace("#episodeTitle#", episode_data["title"])
                    else: 
                        episodes = self.fetch_content_data(
                        title=file_data["title"], season=file_data["season"])
                        episode_data = self.find_correct_episode(episodes)

                        new_filename = new_filename.replace("#episodeTitle#", episode_data["title"])

            if "#season#" in selected_format:
                season = self.file_data["season"]
                if (int(season) <= 9):
                    season = '0' + str(season)

                new_filename = new_filename.replace(
                    "#season#", season)

            if ("#episode#" in selected_format):
                episode = self.file_data["episode"]
                if (int(episode) <= 9):
                    episode = '0' + str(episode)

                new_filename = new_filename.replace(
                    "#episode#", episode)

        self.original_filename = self.filename
        self.filename = new_filename

    def rename(self):
        """ 
            Renames filename to selected format
        """
        original_file_full = f'{self.disk}/{"/".join(self.directories)}/{self.original_filename}{self.extension}'
        new_file_full = f'{self.disk}/{"/".join(self.directories)}/{self.filename}{self.extension}'

        print("old", original_file_full)
        print("new", new_file_full)
        os.rename(original_file_full, new_file_full)

    def find_correct_episode(self, episodes):
        for episode in episodes:
            if int(episode["number"]) is int(self.file_data["episode"]):
                return episode
        print("unexpected error: episode not found")