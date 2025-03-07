import tkinter as tk

class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
    def create_cols(self, num_cols, weight=1): # pass number of cols to configure
        for c in range(num_cols):
            self.columnconfigure(c, weight=weight)  
            
    def create_labels(self, labels=[]):
        i = 0
        for label in labels:
            self.label[i] = tk.Label(self, text=label)
            
    def add_border(self):
        return self.config(borderwidth=2, relief='solid')
    
    def label_border(self, label):
        return label.config(borderwidth=2, relief='solid')