# -----------------------------------------------------------
# Bootstrap configuration from env
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
from dotenv import load_dotenv
import os

load_dotenv()

tmdb_api_key = os.getenv("tmdb_api_key")
