# -----------------------------------------------------------
# The movie database class
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import requests
from lib.Cache import Cache
import json
from lib.config import tmdb_api_key

class Tmd(Cache):
    api_key = tmdb_api_key
    api_url = f'https://api.themoviedb.org/3'

    def fetch_content_data(self, title="", season=None):
        """ 
            Fetches data from TMDB api
        """
        content_type = "movie" if season == None else "tv"
        output = None

        if (content_type == "tv"):
            query = f"{self.api_url}/search/tv?api_key={self.api_key}&query={title}&page=1"
            res = requests.get(query)

            if (res.ok):
                show_id = dict(res.json())["results"][0]["id"]
                query = f"{self.api_url}/tv/{show_id}/season/{season}?api_key={self.api_key}"
                data_res = requests.get(query)

                if (data_res.ok):
                    output = data_res.json()

        return self.clean_response(output)

    def clean_response(self, response):
        """ 
            Removes redundant information from API response
        """
        episodes = []
        for episode in response["episodes"]:
            output = {}
            output["number"] = episode["episode_number"]
            output["season"] = episode["season_number"]

            if "name" in episode:
                output["title"] = episode["name"]
            else:
                output["title"] = None
            episodes.append(output)

        self.add_to_cache(episodes)
        return episodes
