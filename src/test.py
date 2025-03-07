from database.config import DatabaseUser
from database.query import QueryPlayer, QueryTeam
from data_handling.cleaning import clean_floats

TEST_PLAYER_QUERIES = QueryPlayer()

# player_pg_df = DatabaseUser.execute_sys_query(TEST_PLAYER_QUERIES.player_pg, 'LeBron James')
# print(player_pg_df)

def test_get_player_pg():
        db_df = DatabaseUser.execute_sys_query(TEST_PLAYER_QUERIES.player_pg, 'LeBron James')
        df = clean_floats(db_df)
        print(df)
        return df

print(test_get_player_pg())

# import pandas as pd
# from database.config import DatabaseUser
# from database.query import *

# team_totals_query = """
#                 select distinct gl.team as TeamAbb, (td.city || ' ' || td.name) as TeamName,
#                 count(distinct gl.gid) as GamesPlayed, max(gl.game_date) as RecentGame
#                 from pr.current_game_logs gl
#                 inner join tm.team_details td on gl.team = td.team
#                 where gl.team = :1
#                 group by gl.team, (td.city || ' ' || td.name)
#                 """


# # df = DatabaseUser.execute_sys_query(query=team_totals_query, condition='BOS')
# # print(df)

# # team_dash_df = DatabaseUser.execute_sys_query(team_dash, 'MIN')
# # print(team_dash_df)

# player_dash_df = DatabaseUser.execute_sys_query(player_dash, 'LeBron James')
# # print(player_dash_df)

# player_pg_df = DatabaseUser.execute_sys_query(player_pg, 'LeBron James')
# # print(player_pg_df)

# # num_df = player_pg_df.select_dtypes('Float64')
    
# # print(len(num_df.columns))

# # for i in range(len(num_df.columns)):
# #     pcts = ['FGP', 'F3P', 'FTP']
# #     if num_df.columns[i] in pcts:
# #         num_df[num_df.columns[i]] = num_df[num_df.columns[i]].round(4) * 100
# #     else:
# #         num_df[num_df.columns[i]] = num_df[num_df.columns[i]].round(2)  
    
# def clean_floats(df):
#     num_df = df.select_dtypes(include='Float64')
#     notnum_df = df.select_dtypes(exclude='Float64')
#     print(num_df)
#     print(notnum_df)
#     pcts = ['FGP', 'F3P', 'FTP']
#     for i in range(len(num_df.columns)):
#         if num_df.columns[i] in pcts:
#             num_df[num_df.columns[i]] = (num_df[num_df.columns[i]].round(4) * 100).to_string(index=False) + '%'
#         else:
#             num_df[num_df.columns[i]] = num_df[num_df.columns[i]].round(2)
            
#     clean_df = pd.concat([notnum_df, num_df], axis=1) # axis=1 makes it concat along columns instead of rows
    
#     return clean_df
    
# clean_df = clean_floats(player_pg_df)
# print(clean_df)
    
# # print(num_df)