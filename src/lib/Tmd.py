# -----------------------------------------------------------
# The movie database class
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import requests
from lib.Cache import Cache
from lib.config import tmdb_api_key, tmdb_api_url


class Tmd():

    @staticmethod
    def fetch_tv_show(title):
        """ 
            Fetches  data for a tv show from TMDB api
        """
        query = f"{tmdb_api_url}/search/tv?api_key={tmdb_api_key}&query={title}&page=1"
        res = requests.get(query)

        if res.ok:
            return dict(res.json())["results"]
        else:
            return None

    @staticmethod
    def fetch_season(show, season, cache=False):
        """ 
            Fetches season data for a show from TMDB api
        """
        show_id = show["id"]
        query = f"{tmdb_api_url}/tv/{show_id}/season/{season}?api_key={tmdb_api_key}"
        data_res = requests.get(query)

        if data_res.ok:
            output = data_res.json()

        episodes = Tmd.clean_response(output, show["name"])

        if cache is True:            
            cache = Cache.read_from_cache()

            if cache != -1:
                cache[str(season)] = episodes
                Cache.add_to_cache(cache)
            else:
                Cache.add_to_cache({str(season): episodes})

        return episodes

    @staticmethod
    def clean_response(response, title):
        """ 
            Removes redundant information from API response
        """
        episodes = []
        for episode in response["episodes"]:
            output = {"episode": episode["episode_number"],
                      "season": episode["season_number"],
                      "year": episode["air_date"][0:4], #getting year only
                      "title": title
                      }

            if "name" in episode:
                output["episodeTitle"] = episode["name"]
            else:
                output["episodeTitle"] = None
            episodes.append(output)
        return episodes
