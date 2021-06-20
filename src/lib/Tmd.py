# -----------------------------------------------------------
# The movie database class
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import requests
from lib.Cache import Cache
from lib.config import tmdb_api_key, tmdb_api_url


class Tmd():

    @staticmethod
    def fetch_tv_season(title="", season=None):
        """ 
            Fetches data from TMDB api
        """
        content_type = "movie" if season is None else "tv"
        output = None

        if content_type == "tv":
            query = f"{tmdb_api_url}/search/tv?api_key={tmdb_api_key}&query={title}&page=1"
            res = requests.get(query)
            print(query)

            if res.ok:
                # TODO: check if response is empty, if it is then prompt user to enter title
                show_id = dict(res.json())["results"][0]["id"]
                query = f"{tmdb_api_url}/tv/{show_id}/season/{season}?api_key={tmdb_api_key}"
                data_res = requests.get(query)

                if data_res.ok:
                    output = data_res.json()

        episodes = Tmd.clean_response(output)
        Cache.add_to_cache(episodes)

        return episodes

    @staticmethod
    def clean_response(response):
        """ 
            Removes redundant information from API response
        """
        episodes = []
        for episode in response["episodes"]:
            output = {"episode": episode["episode_number"], "season": episode["season_number"]}

            if "name" in episode:
                output["episodeTitle"] = episode["name"]
            else:
                output["episodeTitle"] = None
            episodes.append(output)
        return episodes
