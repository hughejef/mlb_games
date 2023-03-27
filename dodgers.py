import statsapi
import datetime
from datetime import timedelta


# date stuff


class DodgerGame:
    """A Dodger Game object"""
    def __init__(self, game_id, game_day, game_time, home_or_away):
        self.__game_id = game_id
        self.__game_day = game_day
        self.__game_time = game_time
        self.__home_or_away = home_or_away

    def get_game_id(self):
        return self.__game_id

    def get_game_day(self):
        return self.__game_day

    def get_game_time(self):
        return self.__game_time

    def get_home_or_away(self):
        return self.__home_or_away

def check_games():
    game_sched = statsapi.schedule(start_date=str(datetime.date.today()), end_date=str(datetime.date.today()+timedelta(days=7)), team=119)
    for game in game_sched:
        DodgerGame(game['game_id'],game['game_date'],game['game_datetime'],game['away_name'])



check_games()

print(DodgerGame)






#get today

#get tomorrow

team = {}
sched = statsapi.schedule(start_date='03/25/2023',end_date='03/27/2023',team=119)
box_score = statsapi.boxscore_data(719413,timecode=None)
