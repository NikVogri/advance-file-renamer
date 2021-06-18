# -----------------------------------------------------------
# Cache class for local caching
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import pathlib
import json
import os


class Cache:
    path = pathlib.Path().absolute()
    dir = 'cache'

    def add_to_cache(self, to_cache, name="main.txt"):
        """ 
            Writes value to file used for caching
        """
        try:
            with open(f'{self.path}\\{self.dir}\\{name}', 'w') as cache_file:
                cache_file.write(json.dumps(to_cache))
        except FileNotFoundError:
            os.mkdir(f'{self.path}\\{self.dir}')
            with open(f'{self.path}\\{self.dir}\\{name}', 'w') as cache_file:
                print("here")
                cache_file.write(json.dumps(to_cache))

    def read_from_cache(self, name="main.txt"):
        """ 
            Reads from cache file
        """
        try:
            with open(f'{self.path}\\{self.dir}\\{name}', 'r') as cache_file:
                file_content = cache_file.read()
                return json.loads(file_content)
        except FileNotFoundError:
            return -1

    def clear_file_from_cache(self, name="main.txt"):
        if os.path.exists(f'{self.path}\\{self.dir}\\{name}'):
            os.remove(f'{self.path}\\{self.dir}\\{name}')
