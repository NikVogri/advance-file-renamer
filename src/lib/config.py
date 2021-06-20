# -----------------------------------------------------------
# Bootstrap configuration from env
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

tmdb_api_key = os.getenv("tmdb_api_key")
tmdb_api_url = 'https://api.themoviedb.org/3'

supported_file_extensions = [".mp4", ".m4v", ".mkv", ".webm", ".mov", ".avi", ".wmv", ".mpg", ".flv", ".srt"]

cache_location = f"{pathlib.Path().absolute()}\\cache"