import cx_Oracle
import pandas as pd

class DatabaseUser: 
    def __init__(self, username, password, dsn, encoding, mode=None):
        self.username = username
        self.password = password or 'ora'
        self.dsn = dsn or 'localhost/nba_db'
        self.encoding = encoding or 'UTF-8'
        self.mode = mode or cx_Oracle.DEFAULT_AUTH

    @classmethod
    def nba_sys(cls):
        return cls(username='sys', password='orasys', dsn=None, encoding=None, mode=cx_Oracle.SYSDBA)
    
    @classmethod
    def nba_player(cls):
        return cls(username='nbaPlayer', password=None, dsn=None, encoding=None, mode=None)
    
    @classmethod
    def nba_team(cls):
        return cls(username='nbaTeam', password=None, dsn=None, encoding=None, mode=None)
    
    @classmethod
    def nba_game(cls):
        return cls(username='nbaGame', password=None, dsn=None, encoding=None, mode=None)
    
    @classmethod
    def nba_season(cls):
        return cls(username='nbaSeason', password=None, dsn=None, encoding=None, mode=None)
    
    def connect(self):
        connection = None
        try: 
            connection = cx_Oracle.connect(user=self.username,
                                           password=self.password,
                                           dsn=self.dsn, 
                                           encoding=self.encoding,
                                           mode=self.mode
                                           )
        except cx_Oracle.Error as e:
            print(e)
        return connection
    
    @staticmethod
    def disconnect(connection):
        connection.close()
        # print('disconnected')
    
    @classmethod
    def execute_sys_query(cls, query, condition=None):
        connection = cls.connect(cls.nba_sys())
        cursor = connection.cursor()
        if condition: 
            result = cursor.execute(query, (condition,)).fetchall()
        else:
            result = cursor.execute(query).fetchall()
          
        df = pd.DataFrame.from_records(result, columns=[x[0] for x in cursor.description])
        
        cursor.close()
        cls.disconnect(connection)
        
        return df
    
    @classmethod
    def get_single_record(cls, query, condition=None):
        connection = cls.connect(cls.nba_sys())
        cursor = connection.cursor()
        if condition: 
            result = cursor.execute(query, (condition,)).fetchone()
        else:
            result = cursor.execute(query).fetchone()
            
        # print(result)
        return result
            
    @staticmethod
    def execute_query(connection, query, condition=None):
        cursor = connection.cursor()
        if condition: 
            result = cursor.execute(query, (condition,)).fetchall()
        else:
            result = cursor.execute(query).fetchall()
        cursor.close()
        
        df = pd.DataFrame.from_records(result, columns=[x[0] for x in cursor.description])
        return df