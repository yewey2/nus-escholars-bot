# Sets up players with data structure

import os
from dotenv import load_dotenv
load_dotenv()

from Player import Player
from PlayersMap import PlayersMap

PLAYERS_LEVEL_1 = os.environ.get('PLAYERS_LEVEL_1')
PLAYERS_LEVEL_2 = os.environ.get('PLAYERS_LEVEL_2')
PLAYERS_LEVEL_3 = os.environ.get('PLAYERS_LEVEL_3')

def setup(pl1 = PLAYERS_LEVEL_1, pl2 = PLAYERS_LEVEL_2, pl3 = PLAYERS_LEVEL_3):
    """Sets up players with data structure"""
    pm1 = PlayersMap(pl1)
    pm2 = PlayersMap(pl2)
    pm3 = PlayersMap(pl3)
    return (
        pm1,
        pm2,
        pm3,
        PlayersMap(dict(pm1.get_players_map(), **pm2.get_players_map(), **pm3.get_players_map()))
    )
    