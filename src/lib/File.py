import tkinter as tk


class File:
    files = []
    updates_files = []

    def addFiles(self, files):
        files_list = list(files)

        for file in files_list:
            self.files.append(self.seperatePath(file))

    def removeFiles(self, files_to_remove=[]):
        if (len(files) > 0):
            self.files = self.files.filter(lambda file: file not in files_to_remove)
        else:
            self.files.clear()

    def renderFilenames(self, frame):
        for label in frame.winfo_children():
            if (isinstance(label, tk.Label)):
                label.destroy()

        for filename in self.files:
            label = tk.Label(frame, text=filename["filename"], width=100)
            label.pack()

    def seperatePath(self, filename):
        seperated_path = filename.split('/')

        disk = seperated_path[0]
        directories = seperated_path[1:-1]
        filename = seperated_path[-1]

        return {
            "disk": disk,
            "directories": directories,
            "filename": filename
        }
