import pathlib
from datetime import datetime

class Error:
    def __init__(self, error):
        self.error = error

    def log_to_file(self):
        with open(f"{pathlib.Path().absolute()}/logs.txt", "w") as log_file:
            log_file.write(f"{datetime.now().strftime(('%Y-%m-%dT%H:%M:%S.%f%z'))}: {str(self.error)}")