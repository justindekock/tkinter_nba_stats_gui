import tkinter as tk

from utility import TITLE_FONT, STITLE_FONT, BUTTON_FONT
from frames.header import Header
from frames.search_menu import SearchMenu
from frames.result_frame import ResultsFrame
from frames.menu import TopMenu

# function that starts the window - runs with if __name__ == '__main__'
def main(): # pass text into Window() to create the instance
    nba_stats_gui = Window('NBA Player Current Stats Lookup')
    nba_stats_gui.mainloop()     

# WINDOW ---------------------------------------------------------------------------------------------
class Window(tk.Tk): # inherits tk, tk is the parent
    def __init__(self, app_text):
        super().__init__() # initialize the tk.TK parent, creates window
        
        self.title(app_text) # text passed when calling App
        self.geometry('1300x840')
        
        self.bind('<KeyPress>', self.keybind)
        
        self.menubar = TopMenu(self)
        
        self.header = Header(self, text="Search my database to view current NBA stats!", font=TITLE_FONT)
        self.header.pack()
        
        self.search_menu_entry_text = "Enter Player's Name (first and last):"
        self.search_menu = SearchMenu(self, prompt_text=self.search_menu_entry_text, 
                                      prompt_font=STITLE_FONT, button_font=BUTTON_FONT)
        self.search_menu.pack(fill='x', pady=5)

        self.result_frame = ResultsFrame(self)
        self.result_frame.pack(fill='both', padx=5, pady=10)
        
    # GLOBAL KEYBINDS - COMMANDS ARE MADE IN OTHER CLASSES BUT INITIATED WITH GLOBAL BINDS
    def keybind(self, event):
        # print(event.state)
        if event.state == 8 and event.keysym == 'Escape': # escape to exit app
            self.destroy()
        if event.state == 262152 and event.keysym == 'Delete': # delete to clear text box
            self.search_menu.clear()
            pass
        if event.state == 12 and event.keysym == 'Return': # ctrl+enter to search
            self.search_menu.get_entry()
            pass
        if event.state == 12 and event.keysym == 'r': # ctrl+r to search random
            self.search_menu.random_entry()
            
# run the app
if __name__ == '__main__':
    main()     