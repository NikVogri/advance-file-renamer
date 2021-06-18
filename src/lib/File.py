# -----------------------------------------------------------
# File class wrapper
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import PTN
import os
import shutil
from lib.Tmd import Tmd
from lib.Cache import Cache
from lib.FilePath import FilePath


class File(Tmd, Cache):
    supported_file_extensions = [".mp4", ".m4v", ".mkv", ".webm", ".mov", ".avi", ".wmv", ".mpg", ".flv", ".srt"]

    def __init__(self, original_file_path):
        self.original_file_path = original_file_path

        path, extension = os.path.splitext(self.original_file_path)

        seperated_path = path.split('/')

        self.extension = extension

        self.original_path = FilePath(path)

        self.filename = seperated_path[-1]
        self.original_filename = seperated_path[-1]

        self.file_data = self.parse_filename()
        self.content_type = "tv" if "season" in self.file_data else "movie"

    def parse_filename(self):
        """ 
            Extracts data from filename
        """
        parsed_filename = PTN.parse(self.filename)
        print(parsed_filename)
        for key, val in parsed_filename.items():
            if isinstance(val, int):
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
        # TODO: better mapping system

        if self.filename == selected_format or selected_format == "":
            return

        if self.extension not in self.supported_file_extensions:
            print(self.extension)
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
            if "#title#" in selected_format:
                new_filename = new_filename.replace(
                    "#title#", self.file_data["title"])

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
                if int(season) <= 9:
                    season = '0' + str(season)

                new_filename = new_filename.replace(
                    "#season#", season)

            if "#episode#" in selected_format:
                episode = self.file_data["episode"]
                if int(episode) <= 9:
                    episode = '0' + str(episode)

                new_filename = new_filename.replace(
                    "#episode#", episode)

        self.filename = new_filename

    def rename(self, new_path):
        """ 
            Renames filename to selected format
        """
        original_file_full = f'{self.original_path.build_path()}/{self.original_filename}{self.extension}'

        if new_path is None or new_path.build_path() == self.original_path.build_path():
            new_full_path = f'{self.original_path.build_path()}/{self.filename}{self.extension}'
            os.rename(original_file_full, new_full_path)
        else:
            new_built_path = new_path.build_path()

            if "#year#" in new_built_path:
                new_built_path = new_built_path.replace("#year#", self.file_data["year"])

            if "#title#" in new_built_path:
                new_built_path = new_built_path.replace("#title#", self.file_data["title"])

            if "#episodeName#" in new_built_path:
                new_built_path = new_built_path.replace("#episodeName#", self.file_data["episodeName"])

            if "#episode#" in new_built_path:
                new_built_path = new_built_path.replace("#episode#", self.file_data["episode"])

            if "#season#" in new_built_path:
                new_built_path = new_built_path.replace("#season#", self.file_data["season"])

            if os.path.exists(new_built_path) is False:
                os.makedirs(new_built_path, exist_ok=True)

            # TODO: improve this -> placeholder
            if "/" in self.filename:
                self.filename = self.filename.split("/")[-1]

            new_full_path = f'{new_built_path}\\{self.filename}{self.extension}'

            if new_path.disk is not self.original_path.disk:
                shutil.move(original_file_full, new_full_path)
                # TODO: error validation (full disk, etc...)
                # TODO: better UX when moving files
            else:
                os.rename(original_file_full, new_full_path)

    def find_correct_episode(self, episodes):
        # TODO: this shouldn't be here - refactor in future
        for episode in episodes:
            if int(episode["number"]) is int(self.file_data["episode"]):
                return episode
        print("unexpected error: episode not found")
