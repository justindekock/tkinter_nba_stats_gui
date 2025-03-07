import tkinter as tk
from frames.baseframe import BaseFrame

class Header(BaseFrame): # changing to base frame.. 
    def __init__(self, parent, text, font):
        super().__init__(parent)
        self.header_label = tk.Label(self, text=text, font=font)
        self.header_label.pack()