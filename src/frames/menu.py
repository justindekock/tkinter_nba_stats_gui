import tkinter as tk
import sys
from frames.baseframe import BaseFrame
from utility import TITLE_FONT, SBTITLE_FONT, STITLE_FONT, BUTTON_FONT

class TopMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_file_menu()
        self.create_option_menu()
        self.create_preference_menu()
        
        
        self.add_cascade(label='File', menu=self.file_menu)
        self.add_cascade(label='Options', menu=self.option_menu)
        self.add_cascade(label='Preferences', menu=self.pref_menu)
        
        self.master.config(menu=self)
        
    def create_file_menu(self):
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label='Exit', command=self.quit)
        
    def create_option_menu(self):
        self.option_menu = tk.Menu(self, tearoff=False)
        self.option_menu.add_command(label='Test', command=self.test_func)

    def create_preference_menu(self):
        self.pref_menu = tk.Menu(self, tearoff=False)
        self.pref_menu.add_command(label='Test', command=self.test_func)
        
    def quit(self):
        sys.exit(0)
        
    def test_func(self):
        pass