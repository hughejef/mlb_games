import statsapi
import datetime


# date stuff
today = str(datetime.date.today())
game_sched = statsapi.schedule(start_date=today,team=119)

def check_game(day):
    if day == game_sched[0]['game_date']:
        print("Next Game on: ",game_sched[0]['game_date'], "against: ")
    else:
        print("Next Game on: ", game_sched[0]['game_date'])

check_game(today)

print(game_sched[0])

#get today

#get tomorrow

team = {}
sched = statsapi.schedule(start_date='03/25/2023',end_date='03/27/2023',team=119)
box_score = statsapi.boxscore_data(719413,timecode=None)
