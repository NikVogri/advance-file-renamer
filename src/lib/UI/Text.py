# -----------------------------------------------------------
# Tkiner Entry wrapper class
# Author Nik Vogrinec - https://github.com/nikvogri
# -----------------------------------------------------------
from tkinter import Entry, StringVar
from lib.Cache import Cache


class Text(Cache):
    text = None

    def __init__(self, frame, **kwargs):
        self.text = StringVar()
        self.input = Entry(frame, kwargs,  textvariable=self.text)

    def position(self, **kwargs):
        self.input.place(kwargs)
        return self

    def set_cached_value(self):
        cached_text_val = self.read_from_cache(name="format.txt")

        if (cached_text_val != -1):
            self.text.set(cached_text_val)

    def getValue(self, text_type="string"):
        text = self.text.get().strip()

        if type == "number":
            try:
                return int(text)
            except:
                return 0
        else:
            return text
