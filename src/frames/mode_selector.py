import tkinter as tk
from frames.baseframe import BaseFrame

class ModeButtons(BaseFrame):
    def __init__(self, parent, label_font, button_font):
        super().__init__(parent)
        
        self.create_cols(3)
        
        self.mode_label = tk.Label(self, text='Search Mode:', font=label_font)
        
        self.mode_var = tk.IntVar(value=1) # defaults to player mode
        
        self.player_mode = tk.Radiobutton(self, text='Player', variable=self.mode_var, value=1, 
                                          command=self.master.switch_mode, font=button_font)
        self.team_mode = tk.Radiobutton(self, text='Team', variable=self.mode_var, value=2, 
                                        command=self.master.switch_mode, font=button_font)
        
        self.mode_label.pack(side='left', padx=10)
        self.player_mode.pack(side='left')
        self.team_mode.pack(side='left')
