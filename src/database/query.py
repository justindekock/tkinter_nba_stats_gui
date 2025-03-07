class QueryPlayer: # PLAYER QUERIES ----------------------------------------------------
    def __init__(self):
        
        self.from_where = """
                from pr.current_game_logs gl
                where gl.player_name = :1
                group by gl.player_name
                """
        self.all_players = 'select distinct gl.player_name as player from pr.current_game_logs gl'
        self.all_pids = 'select distinct gl.player_name, gl.pid from pr.current_game_logs gl'
        self.player_dash = """
                select gl.player_name as player, max(gl.team) as recent_team,
                (td.city || ' ' || td.name) as team_name,
                count(distinct gl.gid) as games_played, max(gl.game_date) as recent_game
                from pr.current_game_logs gl
                inner join tm.team_details td on gl.team = td.team
                where gl.player_name = :1
                group by gl.player_name, (td.city || ' ' || td.name)
                order by recent_game desc
                """
        self.player_pg = """
                select gl.player_name as player, avg(gl.mins) as min, avg(gl.pts) as pts, avg(gl.ast) as ast,
                avg(gl.reb) as reb, avg(gl.stl) as stl, avg(gl.blk) as blk, avg(gl.tov) as tov
                """ + self.from_where
        self.player_season = """
                select gl.player_name as player, sum(gl.mins) as min, sum(gl.pts) as pts, sum(gl.ast) as ast, 
                sum(gl.reb) as reb, sum(gl.stl) as stl, sum(gl.blk) as blk, sum(gl.tov) as tov
                
                """ + self.from_where
        self.player_shooting = """
                select gl.player_name as player, 
                sum(gl.fgm) as fgm, sum(gl.fga) as fga, 
                sum(gl.fg3m) as f3m, sum(gl.fg3a) as f3a,
                sum(gl.ftm) as ftm, sum(gl.fta) as fta,
                avg(gl.fgm) as fgm_pg, avg(gl.fga) as fga_pg,
                case when sum(gl.fgm) > 0 and sum(gl.fga) > 0 then (sum(gl.fgm) / sum(gl.fga))
                else 0 end as fgp, 
                avg(gl.fg3m) as f3m_pg, avg(fg3a) as f3a_pg,
                case when sum(gl.fg3m) > 0 and sum(gl.fg3a) > 0 then (sum(gl.fg3m) / sum(gl.fg3a))
                else 0 end as f3p, 
                avg(ftm) as ftm_pg, avg(fta) as fta_pg,
                case when sum(gl.ftm) > 0 and sum(gl.fta) > 0 then (sum(gl.ftm) / sum(gl.fta))
                else 0 end as ftp
                """ + self.from_where
        self.player_recent_performance = """
                select sum(gl.pts) as pts
                from pr.current_game_logs gl
                where gl.player_name = :1
                group by gl.player_name, gl.game_date
                order by gl.game_date desc
                FETCH FIRST 1 ROW ONLY
                """ 
                
class QueryTeam: # TEAM QUERIES -------------------------------------------------------------
    def __init__(self):
        self.from_where = """
                from pr.current_game_logs gl
                where gl.team = :1
                group by gl.team
                """    
        self.all_teams = 'select distinct gl.team from pr.current_game_logs gl'
        self.all_tids = 'select distinct gl.team, gl.tid from pr.current_game_logs gl'
        
        self.team_dash = """
                select distinct gl.team as team, (td.city || ' ' || td.name) as team_name,
                count(distinct gl.gid) as games_played, max(gl.game_date) as recent_game
                from pr.current_game_logs gl
                inner join tm.team_details td on gl.team = td.team
                where gl.team = :1
                group by gl.team, (td.city || ' ' || td.name)
                """    
        self.team_shooting_og = """
                select gl.team as team, 
                sum(gl.fgm) as fgm, sum(gl.fga) as fga, 
                sum(gl.fg3m) as f3m, sum(gl.fg3a) as f3a,
                sum(gl.ftm) as ftm, sum(gl.fta) as fta,
                avg(sum(gl.fgm)) as fgm_pg, avg(sum(gl.fga)) as fga_pg, 
                avg(sum(gl.fg3m)) as f3m_pg, avg(sum(gl.fg3a)) as f3a_pg,
                avg(sum(gl.ftm)) as ftm_pg, avg(sum(gl.fta)) as fta_pg,
                case when sum(gl.fgm) > 0 and sum(gl.fga) > 0 then (sum(gl.fgm) / sum(gl.fga))
                else 0 end as fgp, 
                case when sum(gl.fg3m) > 0 and sum(gl.fg3a) > 0 then (sum(gl.fg3m) / sum(gl.fg3a))
                else 0 end as f3p, 
                case when sum(gl.ftm) > 0 and sum(gl.fta) > 0 then (sum(gl.ftm) / sum(gl.fta))
                else 0 end as ftp
                from pr.current_game_logs gl
                where gl.team = :1
                group by gl.team
                """  
        self.team_shooting = """
                SELECT 
                gl.team AS team,
                SUM(gl.fgm) AS fgm, 
                SUM(gl.fga) AS fga, 
                SUM(gl.fg3m) AS f3m, 
                SUM(gl.fg3a) AS f3a,
                SUM(gl.ftm) AS ftm, 
                SUM(gl.fta) AS fta,
                SUM(gl.fgm) / COUNT(DISTINCT gl.gid) AS fgm_pg, 
                SUM(gl.fga) / COUNT(DISTINCT gl.gid) AS fga_pg, 
                SUM(gl.fg3m) / COUNT(DISTINCT gl.gid) AS f3m_pg, 
                SUM(gl.fg3a) / COUNT(DISTINCT gl.gid) AS f3a_pg,
                SUM(gl.ftm) / COUNT(DISTINCT gl.gid) AS ftm_pg, 
                SUM(gl.fta) / COUNT(DISTINCT gl.gid) AS fta_pg,
                CASE 
                        WHEN SUM(gl.fga) > 0 THEN SUM(gl.fgm) * 1.0 / SUM(gl.fga)
                        ELSE 0 
                END AS fgp, 
                CASE 
                        WHEN SUM(gl.fg3a) > 0 THEN SUM(gl.fg3m) * 1.0 / SUM(gl.fg3a)
                        ELSE 0 
                END AS f3p, 
                CASE 
                        WHEN SUM(gl.fta) > 0 THEN SUM(gl.ftm) * 1.0 / SUM(gl.fta)
                        ELSE 0 
                END AS ftp
                FROM pr.current_game_logs gl
                WHERE gl.team = :1
                GROUP BY gl.team
        """
        self.team_pg_og = """
                select gl.team as team, avg(gl.mins) as min_pg, avg(gl.pts) as pts_pg, avg(gl.ast) as ast_pg,
                avg(gl.reb) as reb_pg, avg(gl.stl) as stl_pg, avg(gl.blk) as blk_pg, avg(gl.tov) as tov_pg
                """ + self.from_where
        self.team_pg = """
                select avg(sum(gl.mins)) as min, avg(sum(gl.pts)) as pts, avg(sum(gl.ast)) as ast, avg(sum(gl.reb)) as reb,
                        avg(sum(gl.stl)) as stl, avg(sum(gl.blk)) as blk, avg(sum(gl.tov)) as tov
                from pr.current_game_logs gl
                where gl.team = :1
                group by gl.team, gl.gid
                """
        self.team_season = """
                select sum(gl.mins) as min, sum(gl.pts) as pts, sum(gl.ast) as ast, sum(gl.reb) as reb,
                        sum(gl.stl) as stl, sum(gl.blk) as blk, sum(gl.tov) as tov
                """ + self.from_where
        self.team_avg_score = """
                select avg(sum(gl.pts)) as pts, avg(sum(gl.ast)) as ast, avg(sum(gl.reb)) as reb,
                        avg(sum(gl.stl)) as stl, avg(sum(gl.blk)) as blk, avg(sum(gl.tov)) as tov
                from pr.current_game_logs gl
                where gl.team = :1
                group by gl.team, gl.gid
                """             
        self.recent_matchup = """
                select gl.matchup as matchup
                from pr.current_game_logs gl
                where gl.team = :1
                order by gl.game_date desc
                """ 
        self.recent_opp = """
                SELECT opp.team AS opponent_team
                FROM pr.current_game_logs gl
                JOIN pr.current_game_logs opp
                ON gl.gid = opp.gid
                WHERE gl.team = :1
                AND opp.team <> :1
                ORDER BY gl.game_date DESC
                FETCH FIRST 1 ROW ONLY
                """
        self.team_top_scorer = """
                select gl.team as team, gl.player_name, sum(gl.pts) as total_pts
                from pr.current_game_logs gl
                where gl.team = :1
                group by gl.team, gl.player_name
                order by total_pts desc
                """
        self.team_recent_wl_score = """
                SELECT 
                CASE 
                WHEN SUM(CASE WHEN gl.team = :1 THEN gl.pts ELSE 0 END) 
                > SUM(CASE WHEN gl.team <> :1 THEN gl.pts ELSE 0 END) 
                THEN 'Won' 
                ELSE 'Lost'
                END AS wl, 
                SUM(CASE WHEN gl.team = :1 THEN gl.pts END) || ' - ' ||
                SUM(CASE WHEN gl.team <> :1 THEN gl.pts END) as score
                FROM pr.current_game_logs gl
                WHERE gl.team = :1 OR gl.gid IN (
                SELECT gl2.gid FROM pr.current_game_logs gl2 WHERE gl2.team = :1
                )
                GROUP BY gl.gid
                ORDER BY MAX(gl.game_date) DESC
                fetch first 1 row only
                """
        self.team_record_og = """
                SELECT 
                
                COUNT(CASE WHEN 
                        SUM(CASE WHEN gl.team = :1 THEN gl.pts ELSE 0 END) >
                        SUM(CASE WHEN gl.team <> :1 THEN gl.pts ELSE 0 END)
                        then DISTINCT gl.gid) end as wins 
                        
                FROM pr.current_game_logs gl
                WHERE gl.team = :1 OR gl.gid IN (
                SELECT gl2.gid FROM pr.current_game_logs gl2 WHERE gl2.team = :1
                )
                GROUP BY gl.gid
                """
        self.team_wrecord = """
                SELECT COUNT(*) AS wins
                FROM (
                        SELECT gl.gid,
                        SUM(CASE WHEN gl.team = :1 THEN gl.pts ELSE 0 END) AS team_pts,
                        SUM(CASE WHEN gl.team <> :1 THEN gl.pts ELSE 0 END) AS opp_pts
                        FROM pr.current_game_logs gl
                        WHERE gl.team = :1 OR gl.gid IN (
                                SELECT gl2.gid 
                                FROM pr.current_game_logs gl2 
                                WHERE gl2.team = :1
                        )       
                        GROUP BY gl.gid
                ) game_totals
                WHERE team_pts > opp_pts
                """
        self.team_lrecord = """
                SELECT COUNT(*) AS losses
                FROM (
                        SELECT gl.gid,
                        SUM(CASE WHEN gl.team = :1 THEN gl.pts ELSE 0 END) AS team_pts,
                        SUM(CASE WHEN gl.team <> :1 THEN gl.pts ELSE 0 END) AS opp_pts
                        FROM pr.current_game_logs gl
                        WHERE gl.team = :1 OR gl.gid IN (
                                SELECT gl2.gid 
                                FROM pr.current_game_logs gl2 
                                WHERE gl2.team = :1
                        )       
                        GROUP BY gl.gid
                ) game_totals
                WHERE team_pts < opp_pts
                """
        self.team_avg_scores = """
                SELECT 
                AVG(SUM(CASE WHEN gl.team = :1 THEN gl.pts END)) as team_pts,
                AVG(SUM(CASE WHEN gl.team <> :1 THEN gl.pts END)) as opp_pts
                FROM pr.current_game_logs gl
                WHERE gl.team = :1 OR gl.gid IN (
                SELECT gl2.gid FROM pr.current_game_logs gl2 WHERE gl2.team = :1
                )
                GROUP BY gl.gid
                """