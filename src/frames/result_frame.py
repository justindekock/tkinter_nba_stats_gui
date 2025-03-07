import tkinter as tk
from frames.baseframe import BaseFrame
from data_handling.player import PlayerResults
from utility import SBTITLE_FONT

class ResultsFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.dashboard = Dashboard(self)
        self.shooting = ShootingStats(self)
        self.pergame = StatsPerGame(self)
        self.totals = StatsTotals(self)
        
        self.shooting.add_border()
        self.pergame.add_border()
        self.totals.add_border()
        
        self.dashboard.pack(fill='x')
        self.shooting.pack(side='bottom', fill='x', pady=10)
        self.pergame.pack(side='left', pady=5, padx=100)
        self.totals.pack(side='right', pady=5, padx=100)
        
    # TODO - when in team mode, give option to view top player's stats
class Dashboard(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_cols(5)
        self.labels = []
        self.results = None
        
    def update_dashboard(self, mode, results):
        font = SBTITLE_FONT
        sticky = 'nsew'
        padx = 25
        pady = 5
        
        self.results = results
        self.player = self.results.player if mode == 1 else self.results.top_scorer[1]
        self.team = f'{self.results.player_dash[2][1]} ({self.results.player_dash[1][1]})' if mode ==1 \
            else f'{self.results.team_dash[1]} ({self.results.team_dash[0]})'
         
        # get player (or top scorer) and team images
        self.team_logo = self.results.player_team_results.team_logo if mode == 1 else self.results.team_logo
        if mode == 1:
            self.headshot = self.results.headshot
        else:
            self.ts_results = PlayerResults(self.player) # make player class for top scorer to get their photo
            self.headshot = self.ts_results.headshot
        
        # variables from results class instance (player or team)
        self.gp = f'{self.results.player_dash[3][1] if mode == 1 else self.results.team_dash[2]} Games Played'
        self.lg = self.results.player_dash[4][1].strftime('%m-%d-%Y') if mode == 1\
            else self.results.team_dash[3].strftime('%m-%d-%Y')
        self.record = self.results.player_team_results.team_record if mode == 1 else self.results.team_record
        self.recent_wl = self.results.player_team_results.recent_wl_score[0] if mode == 1 else self.results.recent_wl_score[0]
        self.recent_score = self.results.player_team_results.recent_wl_score[1] if mode == 1 else self.results.recent_wl_score[1]
        self.recent_opp = self.results.player_team_results.recent_opp if mode == 1 else self.results.recent_opp
        self.ts_pts = None if mode == 1 else self.results.top_scorer[2]
        self.recent_pts = self.results.player_recent if mode == 1 else None
        
        # strings for labels
        player_text = f'{self.player}' if mode == 1 else f'Top Scorer: {self.player} ({self.ts_pts} pts)'
        record_text = f'{self.record} ({self.gp})'
        if mode == 1:
            recent_text = f'Recently scored {self.recent_pts} point(s) in {self.recent_score} {"win" if self.recent_wl == 'Won' else "loss"} against {self.recent_opp} on {self.lg}'
        else:
            recent_text = f'Recently {"Beat" if self.recent_wl == 'won' else "lost to"} {self.recent_opp} ({self.recent_score}) on {self.lg}'
        
        # destroy existing labels 
        for label in self.labels:
            label.destroy()
        self.labels.clear()
        
        # images (logo on left for player, on right for player)
        logo_label = tk.Label(self, image=self.team_logo, anchor='e' if mode == 1 else 'w')
        headshot_label = tk.Label(self, image=self.headshot, anchor='w' if mode == 1 else 'e')
        
        # text labels
        team_label = tk.Label(self, text=self.team, font=font)
        player_label = tk.Label(self, text=player_text, font=font)
        gp_label = tk.Label(self, text=self.gp, font=font)
        lg_label = tk.Label(self, text=f'Last Game Played: {self.lg}', font=font)
        record_label = tk.Label(self, text=record_text, font=font)
        recent_label = tk.Label(self, text=recent_text, font=font)
        self.labels.append(logo_label)
        self.labels.append(headshot_label)
        self.labels.append(team_label)
        self.labels.append(player_label)
        self.labels.append(gp_label)
        self.labels.append(lg_label)
        self.labels.append(record_label)
        self.labels.append(recent_label)
        
        if mode == 1: # player name on top, logo left headshot right
            player_label.grid(row=0, column=0, columnspan=6, sticky=sticky, padx=padx, pady=pady)
            logo_label.grid(row=1, column=0, columnspan=3, sticky=sticky)
            headshot_label.grid(row=1, column=3, columnspan=2, sticky=sticky)
            team_label.grid(row=2, column=0, columnspan=3, sticky=sticky, padx=padx, pady=pady)
            
        else: # team name on top, headshot left logo right
            team_label.grid(row=0, column=0, columnspan=6, sticky=sticky, padx=padx, pady=pady)
            headshot_label.grid(row=1, column=0, columnspan=3, sticky=sticky)
            logo_label.grid(row=1, column=3, columnspan=2, sticky=sticky)
            player_label.grid(row=2, column=0, columnspan=3, sticky=sticky, padx=padx, pady=pady)
            
        record_label.grid(row=2, column=3, columnspan=3, sticky=sticky, padx=padx, pady=pady)
        recent_label.grid(row=3, column=0, columnspan=6, sticky=sticky, padx=padx, pady=pady)
        
        for label in self.labels: # add labels to all except the images
            if label == logo_label or label == headshot_label:
                pass
            else:
                self.label_border(label)
            
class ShootingStats(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_cols(6)
        self.labels = []
        
    def update_shooting(self, df, font):

        def shooting_labels(self, df, start_row, start_col):
            for i, col in enumerate(df.columns):
                col_text = f'{str(col):>6}: '
                val_text = str(df[col].values[0])
                
                col_lbl = tk.Label(self, text=col_text, font=font, anchor='e', width=10)
                self.labels.append(col_lbl)
                val_lbl = tk.Label(self, text=val_text, font=font, anchor='w', width=5)
                self.labels.append(val_lbl)
                
                col_lbl.grid(row=start_row, column=start_col, sticky='e')
                val_lbl.grid(row=start_row, column=start_col + 1, sticky='w')
                
                start_row += 1
                
        self.fg_label = tk.Label(self, text='Field Goal Shooting:', font=SBTITLE_FONT)
        self.f3_label = tk.Label(self, text='Three Point Shooting:', font=SBTITLE_FONT)
        self.ft_label = tk.Label(self, text='Free Throw Shooting:', font=SBTITLE_FONT)
        sh_title_sticky = 'nsew'
        self.fg_label.grid(row=0, column=0, columnspan=2, sticky=sh_title_sticky)
        self.f3_label.grid(row=0, column=2, columnspan=2, sticky=sh_title_sticky)
        self.ft_label.grid(row=0, column=4, columnspan=2, sticky=sh_title_sticky)
        
        self.fg_df = df[['FGM_PG', 'FGA_PG', 'FGM', 'FGA']]
        self.f3_df = df[['F3M_PG', 'F3A_PG', 'F3M', 'F3A']]
        self.ft_df = df[['FTM_PG', 'FTA_PG', 'FTM', 'FTA']]
        
        self.fgp_label = tk.Label(self, text=f"Efficiency: {df['FGP'].values[0]}", font=SBTITLE_FONT)
        self.f3p_label = tk.Label(self, text=f"Efficiency: {df['F3P'].values[0]}", font=SBTITLE_FONT)
        self.ftp_label = tk.Label(self, text=f"Efficiency: {df['FTP'].values[0]}", font=SBTITLE_FONT)
        eff_sticky = 'nsew'
        self.fgp_label.grid(row=1, column=0,  sticky=eff_sticky, columnspan=2)
        self.f3p_label.grid(row=1, column=2, sticky=eff_sticky, columnspan=2)
        self.ftp_label.grid(row=1, column=4, sticky=eff_sticky, columnspan=2)
    
        shooting_labels(self, self.fg_df, start_row=2, start_col=0)
        shooting_labels(self, self.f3_df, start_row=2, start_col=2)
        shooting_labels(self, self.ft_df, start_row=2, start_col=4)
        
            
class StatsPerGame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_cols(6)
        self.labels = []
        
    def update_pg(self, df, font):
        for label in self.labels:
            label.destroy()
        
        self.labels.clear()
        
        def pergame_labels(self, df, start_row, start_col):
            for i, col in enumerate(df.columns):
                col_text = f'{str(col):>4}: '
                val_text = str(df[col].values[0])
                
                col_lbl = tk.Label(self, text=col_text, font=font, anchor='e')#, width=10)
                self.labels.append(col_lbl)
                val_lbl = tk.Label(self, text=val_text, font=font, anchor='w', pady=10, padx=5, width=5)#, width=10)
                self.labels.append(val_lbl)
                
                col_lbl.grid(row=start_row, column=start_col, sticky='e', padx=5)
                val_lbl.grid(row=start_row, column=start_col + 1, sticky='w')
                start_col += 1
                
        self.pg_label = tk.Label(self, text='Per-Game Stats:', font=SBTITLE_FONT)
        self.min_label = tk.Label(self, text=f"{df['MIN'].values[0]} Minutes Per-Game", font=SBTITLE_FONT)
        
        sticky = 'nsew'
        center = 20
        self.pg_label.grid(row=0, column=1, columnspan=2, sticky=sticky, padx=center)
        self.min_label.grid(row=1, column=1, columnspan=2, sticky=sticky, padx=center)
        
        self.box_df = df[['PTS', 'AST', 'REB']]
        self.def_df = df[['STL', 'BLK', 'TOV']]
        pergame_labels(self, self.box_df, start_row=2, start_col=0)
        pergame_labels(self, self.def_df, start_row=3, start_col=0)
                
class StatsTotals(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_cols(6)
        self.labels = []
        
    def update_totals(self, df, font):
        for label in self.labels:
            label.destroy()
        
        self.labels.clear()
        
        def totals_labels(self, df, start_row, start_col):
            for i, col in enumerate(df.columns):
                col_text = f'{str(col)}:'
                val_text = str(df[col].values[0])

                
                col_lbl = tk.Label(self, text=col_text, font=font, anchor='e')#, width=10)
                self.labels.append(col_lbl)
                val_lbl = tk.Label(self, text=val_text, font=font, anchor='w', pady=10, padx=5, width=4)#, width=10)
                self.labels.append(val_lbl)
                
                col_lbl.grid(row=start_row, column=start_col, sticky='e')
                val_lbl.grid(row=start_row, column=start_col + 1, sticky='w')
                
                start_col += 1
                
        self.totals_label = tk.Label(self, text='Seaon Totals:', font=SBTITLE_FONT)
        self.mins_label = tk.Label(self, text=f"{df['MIN'].values[0]} Minutes Played", font=SBTITLE_FONT)
        
        sticky = 'nsew'
        center = 20
        
        self.totals_label.grid(row=0, column=1, columnspan=2, sticky=sticky, padx=center)
        self.mins_label.grid(row=1, column=1, columnspan=2, sticky=sticky, padx=center)
        
        self.box_df = df[['PTS', 'AST', 'REB']]
        self.def_df = df[['STL', 'BLK', 'TOV']]
        
        totals_labels(self, self.box_df, start_row=2, start_col=0)
        totals_labels(self, self.def_df, start_row=3, start_col=0)
    
        
        