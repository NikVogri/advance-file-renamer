import os
class FilePath():
    def __init__(self, full_path):
        split_path = full_path.split('/')
        self.disk = split_path[0]
        self.directories = split_path[1:-1]

    def build_path(self):
        sep = os.path.sep
        return f"{self.disk}{sep}{sep.join(self.directories)}"

    def path_exists(self):
        return os.path.exists(self.build_path())