from PIL import Image, ImageTk
 
from database.config import DatabaseUser
from database.query import QueryTeam
from data_handling.cleaning import clean_floats

TEAM_QUERIES = QueryTeam()

class Teams:
    def __init__(self):
        self.teams = []
        self.tids = []
        
    def get_teams(self):
        self.teams = DatabaseUser.execute_sys_query(TEAM_QUERIES.all_teams).values.flatten().tolist()
        return self.teams
    
    def get_tids(self):
        self.tids = DatabaseUser.execute_sys_query(TEAM_QUERIES.all_tids)
        return self.tids
    
class TeamResults:
    def __init__(self, team):
        self.team = team
        self.team_logo = self.get_logo()
        self.team_dash = self.get_team_dash()
        self.team_pg = self.get_team_pg()
        self.team_season = self.get_team_season()
        self.team_shooting = self.get_team_shooting()
        self.top_scorer = self.get_top_scorer()
        self.team_record = self.get_team_record()
        self.team_avg_score = self.get_avg_scores()
        self.recent_matchup = self.get_recent_matchup()
        self.recent_opp = self.get_recent_opp()
        self.recent_wl_score = self.get_recent_wl_score()
        
    def get_team_dash(self):
        self.df = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_dash, self.team)
        return self.df.values.flatten().tolist()
    
    def get_logo(self):
        logo_path = fr'images\team_logos\{self.team}_logo.png'
        logo = Image.open(logo_path).resize((150, 150))
        logo_tk = ImageTk.PhotoImage(logo) 
        return logo_tk
    
    def get_top_scorer(self):
        self.top_scorer = DatabaseUser.get_single_record(TEAM_QUERIES.team_top_scorer, self.team)
        return self.top_scorer
    
    def get_record(self):
        self.wl_record = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_record, self.team)
        return self.wl_record
    
    def get_team_pg(self):
        self.df = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_pg, self.team)
        self.df = clean_floats(self.df)
        return self.df
    
    def get_team_season(self):
        self.df = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_season, self.team)
        return self.df
        
    def get_team_shooting(self):
        self.df = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_shooting, self.team)
        self.df = clean_floats(self.df)
        self.df = self.df.reset_index(drop=True)
        return self.df
    
    def get_avg_scores(self):
        self.scores = DatabaseUser.get_single_record(TEAM_QUERIES.team_avg_scores, self.team)
        self.scores = [round(float(self.scores[0])), round(float(self.scores[1]))]
        return self.scores
    
    def get_recent_matchup(self):
        self.matchup = DatabaseUser.get_single_record(TEAM_QUERIES.recent_matchup, self.team)
        return self.matchup[0]
    
    def get_recent_opp(self):
        self.opp = DatabaseUser.get_single_record(TEAM_QUERIES.recent_opp, self.team)
        return self.opp[0].strip()
    
    def get_recent_wl_score(self):
        self.wl_score = DatabaseUser.execute_sys_query(TEAM_QUERIES.team_recent_wl_score, self.team)
        self.wl_score = self.wl_score.values.flatten().tolist()
        return self.wl_score
    
    def get_team_record(self):
        self.wrecord = DatabaseUser.get_single_record(TEAM_QUERIES.team_wrecord, self.team)[0]
        self.lrecord = DatabaseUser.get_single_record(TEAM_QUERIES.team_lrecord, self.team)[0]
        self.record = f'{self.wrecord} Wins - {self.lrecord} Losses'
        return self.record