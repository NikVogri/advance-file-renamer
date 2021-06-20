# -----------------------------------------------------------
# Cache class for local caching
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import json
import os
from lib.config import cache_location


class Cache:

    @staticmethod
    def add_to_cache(to_cache, name="main.txt"):
        """ 
            Writes value to file used for caching
        """
        try:
            with open(f'{cache_location}\\{name}', 'w') as cache_file:
                cache_file.write(json.dumps(to_cache))
        except FileNotFoundError:
            os.mkdir(f'{cache_location}')
            with open(f'{cache_location}\\{name}', 'w') as cache_file:
                cache_file.write(json.dumps(to_cache))

    @staticmethod
    def read_from_cache(name="main.txt"):
        """ 
            Reads from cache file
        """
        try:
            with open(f'{cache_location}\\{name}', 'r') as cache_file:
                file_content = cache_file.read()
                return json.loads(file_content)
        except FileNotFoundError:
            return -1

    @staticmethod
    def clear_file_from_cache(name="main.txt"):
        if os.path.exists(f'{cache_location}\\{name}'):
            os.remove(f'{cache_location}\\{name}')
