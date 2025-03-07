from PIL import Image, ImageTk 
from unidecode import unidecode

from database.config import DatabaseUser
from database.query import QueryPlayer
from data_handling.cleaning import clean_floats
from data_handling.team import TeamResults

PLAYER_QUERIES = QueryPlayer()

class Players:
    def __init__(self):
        self.players = []
        self.players_norm = []
        
    def get_players(self):
        self.players = DatabaseUser.execute_sys_query(PLAYER_QUERIES.all_players).values.flatten().tolist()
        return self.players
    
    def get_players_norm(self): # players in normalized format no accidentals
        self.df = DatabaseUser.execute_sys_query(PLAYER_QUERIES.all_players)
        self.df['player_norm'] = self.df['PLAYER'].apply(lambda x: unidecode(x.lower()))
        return self.df

    def get_pids(self):
        self.pids = DatabaseUser.execute_sys_query(PLAYER_QUERIES.all_pids)
        return self.pids

class PlayerResults:
    def __init__(self, player):
        self.player = player
        self.headshot = self.get_headshot()
        self.player_dash = self.get_player_dash()
        self.player_pg = self.get_player_pg()
        self.player_season = self.get_player_season()
        self.player_shooting = self.get_player_shooting()
        self.player_team = self.get_team()
        self.player_recent = self.get_player_recent()
        self.player_team_results = TeamResults(self.player_team) # create instance of team results based on player searched
        
    def get_team(self):
        self.team = self.player_dash[1][1]
        return self.team
    
    def get_headshot(self):
        player_ = unidecode(self.player.lower().replace(' ', '_').replace('.', ''))
        player_path = fr'images\player_headshots\{player_}.png'
        headshot = Image.open(player_path).resize((206, 150)) # 137, 150
        headshot_tk = ImageTk.PhotoImage(headshot) 
        return headshot_tk

    def get_player_dash(self):
        self.df = DatabaseUser.execute_sys_query(PLAYER_QUERIES.player_dash, self.player)
        self.cols = self.df.columns.tolist()
        self.vals = self.df.values.flatten().tolist()
        self.cols_vals = list(zip(self.cols, self.vals))
        return self.cols_vals
    
    def get_player_pg(self):
        self.df = DatabaseUser.execute_sys_query(PLAYER_QUERIES.player_pg, self.player)
        self.df = clean_floats(self.df)
        return self.df
    
    def get_player_season(self):
        self.df = DatabaseUser.execute_sys_query(PLAYER_QUERIES.player_season, self.player)
        return self.df
    
    def get_player_shooting(self):
        self.df = DatabaseUser.execute_sys_query(PLAYER_QUERIES.player_shooting, self.player)
        self.df = clean_floats(self.df)
        self.df = self.df.reset_index(drop=True)
        return self.df
    
    def get_player_recent(self):
        self.recent_pts = DatabaseUser.get_single_record(PLAYER_QUERIES.player_recent_performance, self.player)
        return self.recent_pts[0]