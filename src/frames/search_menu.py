import tkinter as tk
import random
from unidecode import unidecode
from frames.baseframe import BaseFrame
from frames.mode_selector import ModeButtons
from utility import SBTITLE_FONT, TEXT_FONT, BUTTON_FONT
from data_handling.player import Players, PlayerResults
from data_handling.team import Teams, TeamResults

class SearchMenu(BaseFrame):
    def __init__(self, parent, prompt_text, prompt_font, button_font):
        super().__init__(parent)
        
        self.create_cols(3)
        self.team_prompt_text = 'Enter NBA Team (abbreviation):'
        self.team_rand_text = 'Search for a Random NBA Team'
        
        self.player_prompt_text = "Enter Player's Name (first and last):"
        self.prompt = tk.Label(self, text=prompt_text, font=prompt_font)
        self.prompt.grid(row=1, column=0, sticky='ew', padx=10)
        
        self.textbox = tk.Text(self, font=prompt_font, height=1, width=40)
        self.textbox.grid(row=1, column=1, sticky='ew')
        self.textbox.focus() # app opens with cursor in textbox
        
        self.search_button = tk.Button(self, text='Search', font=button_font, command=self.get_entry)
        self.search_button.grid(row=1, column=2, sticky='nsew', padx=10)
        
        self.clear_button = tk.Button(self, text='Clear Text', font=button_font, command=self.clear)
        self.clear_button.grid(row=0, column=2, sticky='nsew', padx=10)
        
        self.player_rand_text ='Search for a Random NBA Player'
        self.random_button = tk.Button(self, text=self.player_rand_text, font=button_font, command=self.random_entry)
        self.random_button.grid(row=0, column=1, sticky='w', padx=10)

        self.mode_selector = ModeButtons(self, label_font=SBTITLE_FONT, button_font=TEXT_FONT)
        self.mode_selector.grid(row=0, column=0, sticky='ew', padx=20)
        
    def clear(self):
        self.textbox.delete('1.0', tk.END)
        
    def get_mode(self):
        mode = self.mode_selector.mode_var.get()
        return mode
        
    def switch_mode(self):
        if self.get_mode() == 1:
            self.prompt.config(text=self.player_prompt_text)
            self.random_button.config(text=self.player_rand_text)
        if self.mode_selector.mode_var.get() == 2:
            self.prompt.config(text=self.team_prompt_text)
            self.random_button.config(text=self.team_rand_text)
    
    def random_entry(self):
        if self.get_mode() == 1:
            self.players = Players().get_players()
            self.random_num = random.randint(0, len(self.players)-1) # generate random integer
            self.random_player = self.players[self.random_num] # pass randint as index in player list to get random player
            self.clear()
            self.textbox.insert('1.0', self.random_player)
            self.validate_entry(self.random_player)
        if self.get_mode() == 2:
            self.teams = Teams().get_teams()
            self.random_num = random.randint(0, len(self.teams)-1) # generate random integer
            self.random_team = self.teams[self.random_num]
            self.clear()
            self.textbox.insert('1.0', self.random_team)
            self.validate_entry(self.random_team)
    
    def get_entry(self):
        self.entry = str(self.textbox.get('1.0','end-1c')).strip()
        self.clear()
        self.validate_entry(self.entry)
    
    def validate_entry(self, entry):
        self.mode = self.get_mode()
        self.entry = entry
        if self.mode == 1: # ADDED CODE 2/18 TO ALLOW SEARCHING PLAYER IN WRONG CASE
            self.players = Players().get_players()
            self.players_norm = Players().get_players_norm() # all players in normalized format, lowercase no accidentals
            self.entry_norm = unidecode(self.entry.lower()) # convert entry to same format to allow proper searching regardless of case
            if self.entry_norm in self.players_norm['player_norm'].values.flatten().tolist():
                match_df = self.players_norm[self.players_norm['player_norm'] == self.entry_norm]
                self.player = match_df['PLAYER'].values.tolist()[0] # validate with noramlized format, but pass format from databse to results
                self.results = PlayerResults(self.player)
            else:
                print('invalid player') # TODO - implement error message
        else: 
            self.teams = Teams().get_teams()
            self.entry = self.entry.upper()
            if self.entry in self.teams:
                self.results = TeamResults(self.entry)
            else:
                print('invalid team')
                
        # update results frame with results
        self.master.result_frame.dashboard.update_dashboard(self.mode, self.results)
        self.master.result_frame.pergame.update_pg( 
            self.results.player_pg if self.mode == 1 else self.results.team_pg, font=BUTTON_FONT)
        self.master.result_frame.totals.update_totals(
            self.results.player_season if self.mode == 1 else self.results.team_season, font=BUTTON_FONT)
        self.master.result_frame.shooting.update_shooting(
            self.results.player_shooting if self.mode == 1 else self.results.team_shooting, font=BUTTON_FONT)
        
        self.clear()
