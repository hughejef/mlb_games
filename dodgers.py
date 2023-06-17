import statsapi
import datetime
from datetime import timedelta
https://sftp.amerihome.com/public/file/Twe9VZ-PL0aSmUx4x3J9jw/LeaveOfAbsense.zip
https://sftp.amerihome.com/public/file/cCdFYtUJMU2G9ZrAFcBLwA/PerformanceReviews.zip
# date stuff

class DodgerGame:
    """A Dodger Game object"""
    def __init__(self, game_id, game_day, game_time, home_team):
        self.__game_id = int(game_id)
        self.__game_day = str(game_day)
        self.__game_time = str(game_time)
        self.__home_team = str(home_team)

    def get_game_id(self):
        return self.__game_id

    def get_game_day(self):
        return self.__game_day

    def get_game_time(self):
        return self.__game_time

    def get_home_or_away(self):
        if self.__home_team == 'Los Angeles Dodgers':
            return 'Home'
        else:
            return 'Away'

game_dict = {}
game_list = []

def check_games():
    game_sched = statsapi.schedule(start_date=str(datetime.date.today()), end_date=str(datetime.date.today()+timedelta(days=7)), team=119)
    time_object = str(datetime.datetime.strptime(game_sched[1]['game_datetime'].replace('T',' ').replace('Z',''), '%Y-%m-%d %H:%M:%S')+timedelta(hours=-7))
    time = datetime.datetime.strptime(time_object.split(' ')[1], '%H:%M:%S').time()

    current_game = {'game_id': game_sched[0]['game_id'], 'game_day':game_sched[0]['game_date'], 'game_time': str(time)}
    next_game = {'game_id': game_sched[1]['game_id'], 'game_day':game_sched[1]['game_date'], 'game_time': str(time), 'home_team':game_sched[1]['home_name'], 'away_team':game_sched[1]['away_name']}


    print(next_game)




check_games()



#get today

#get tomorrow

team = {}
sched = statsapi.schedule(start_date='03/25/2023',end_date='03/27/2023',team=119)
box_score = statsapi.boxscore_data(719413,timecode=None)
