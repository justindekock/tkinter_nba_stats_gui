import time
import requests
from cairosvg import svg2png
from unidecode import unidecode
from data_handling.team import Teams
from data_handling.player import Players

def get_team_logos():
    teams = Teams()
    tids = teams.get_tids()

    for tid in tids['TID'].values.flatten().tolist():
        tid = tids[tids['TID'] == tid].values.flatten()[1]
        team = tids[tids['TID'] == tid].values.flatten()[0]
        url = f'https://cdn.nba.com/logos/nba/{tid}/primary/L/logo.svg'
        svg_path = fr'D:\programming_projects\nba_application\images\svg\{team}_logo.svg'
        png_path = fr'D:\programming_projects\nba_application\images\png\{team}_logo.png'
        
        r = requests.get(url)
        svg = r.content
        
        # save svg file
        with open(svg_path, 'wb') as f:
            f.write(svg)
            
        # convert svg to png
        # first have to run these commands: pacman -Syu , # pacman -S mingw-w64-x86_64-cairo
        svg2png(bytestring=svg, write_to=png_path) # had to install build tools, msys2 to get cairo working
            
def get_player_headshots():
    players = Players()
    pids = players.get_pids()
    
    i = 0 
    for pid in pids['PID'].values.flatten().tolist():
        pid = pids[pids['PID'] == pid].values.flatten()[1]
        player = unidecode(pids[pids['PID'] == pid].values.flatten()[0].replace(' ', '_').replace('.', '').lower())
        # unide code converts names like doncic to plain characters

        url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{pid}.png'
        png_path = fr'D:\programming_projects\nba_application\images\player_headshots\{player}.png'
        
        r = requests.get(url)
        print(r.status_code)
        
        with open(png_path, 'wb') as f:
            f.write(r.content)
            
        i += 1
        
        if i % 100 == 0:
            time.sleep(30)
        elif i % 50 == 0:
            time.sleep(10)
        elif i % 25 == 0:
            time.sleep(5)

get_player_headshots()
    