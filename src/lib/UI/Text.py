from tkinter import Entry, StringVar


class Text:
    text = None

    def __init__(self, frame):
        self.text = StringVar()
        self.input = Entry(frame, textvariable=self.text)

    def position(self, **kwargs):
        self.input.place(kwargs)
        return self

    def getValue(self, text_type = "string"):
        text = self.text.get().strip()

        if type == "number":
            try: 
                return int(text)
            except:
                return 0
        else:
            return text
