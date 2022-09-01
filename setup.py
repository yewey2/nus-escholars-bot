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
    return PlayersMap(dict(pm1.get_players_map(), **pm2.get_players_map(), **pm3.get_players_map()))
    return (
        pm1,
        pm2,
        pm3,
        PlayersMap(dict(pm1.get_players_map(), **pm2.get_players_map(), **pm3.get_players_map()))
    )
    
if __name__ == "__main__":
    """Here's an example use case of setup()"""
    print("Running setup.py")
    players = setup('player1,player2,player3','person1,person2,person3','clown1,clown2,clown3')
    
    [print(i) for i in players.get_players_map().items()]
    player1 = players.get('player1')
    print('angel', player1.get_angel().get_username())
    print('mortal', player1.get_mortal().get_chat_id())