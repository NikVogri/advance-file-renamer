# -----------------------------------------------------------
# FilePath class for managing directory paths
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
import os
class FilePath():
    def __init__(self, full_path):
        split_path = full_path.split(os.path.sep)
        self.disk = split_path[0]
        self.directories = split_path[1:-1]

    def build_path(self):
        sep = os.path.sep
        return f"{self.disk}{sep}{sep.join(self.directories)}"

    def exists(self):
        return os.path.exists(self.build_path())

    def create(self):
        os.makedirs(self.build_path(), exist_ok=True)
