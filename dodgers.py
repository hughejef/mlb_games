import statsapi
import datetime
from datetime import timedelta
from tkinter import *
from PIL import Image, ImageTk

# date stuff

class DodgerGame:
    """A Dodger Game object"""
    def __init__(self, game_id, game_day, game_time, home_team, away_team):
        self.__game_id = int(game_id)
        self.__game_day = str(game_day)
        self.__game_time = str(game_time)
        self.__home_team = str(home_team)
        self.__away_team = str(away_team)

    def get_game_id(self):
        return self.__game_id

    def get_game_day(self):
        return self.__game_day

    def get_game_time(self):
        return self.__game_time

    def get_home_team(self):
        return self.__home_team

    def get_away_team(self):
        return self.__away_team


def check_games():
    game_sched = statsapi.schedule(start_date=str(datetime.date.today()), end_date=str(datetime.date.today()+timedelta(days=7)), team=119)
    time_object = str(datetime.datetime.strptime(game_sched[0]['game_datetime'].replace('T',' ').replace('Z',''), '%Y-%m-%d %H:%M:%S')+timedelta(hours=-7))
    time = datetime.datetime.strptime(time_object.split(' ')[1], '%H:%M:%S').time()

    current_game = (int(game_sched[0]['game_id']), game_sched[0]['game_date'], str(time), game_sched[0]['home_name'], game_sched[0]['away_name'])
    next_game = {'game_id': game_sched[1]['game_id'], 'game_day':game_sched[1]['game_date'], 'game_time': str(time), 'home_team':game_sched[1]['home_name'], 'away_team':game_sched[1]['away_name']}
    print(game_sched)
    return current_game



current_game = check_games()

game1 = DodgerGame(current_game[0],current_game[1],current_game[2],current_game[3],current_game[4])

"""
#Create Scoreboard

root = Tk()  # create root window
root.title("Dodger Games")
root.config(bg="blue")
root.geometry("800x480")

# Create base screen
matchupframe = Frame(root)
matchupframe.columnconfigure(0, weight=1)
matchupframe.columnconfigure(1, weight=1)
matchupframe.columnconfigure(2, weight=1)

matchupframe.rowconfigure(1, weight=1)
matchupframe.rowconfigure(2, weight=1)
matchupframe.pack(fill='x')
# Away Team Logo

away_logo_image = Image.open('C:/Users/jchug/PycharmProjects/dodger_games/logos/'+game1.get_away_team()+'.png')
original_away_image = ImageTk.PhotoImage(away_logo_image.resize((100,100)))  # resize image using subsample

label_away = Label(matchupframe, image=original_away_image)
label_away.pack()
label_away.grid(row=0, column=0, sticky="news")

# At
label = Label(matchupframe, text="at", font=('Arial',18), width=42)
label.grid(row=0, column= 1, sticky="news")


# Home Team Logo
home_logo_image = Image.open('C:/Users/jchug/PycharmProjects/dodger_games/logos/'+game1.get_home_team()+'.png')
original_home_image = ImageTk.PhotoImage(home_logo_image.resize((100,100)))  # resize image using subsample
label_home = Label(matchupframe, image=original_home_image)
label_home.grid(row=0, column=2, sticky="news")

# Next Game Time / Date

label = Label(matchupframe, text="Next Game:")
label.grid(row=1, column=1, sticky="EWN",pady=100)

gamedate = Label(matchupframe, text=game1.get_game_day())
gametime = Label(matchupframe, text = game1.get_game_time())
gametime.grid(row = 2, column = 1, sticky="EWN")
gamedate.grid(row=3, column=1, sticky="EWN",)


root.mainloop()
"""
print(game1.get_game_time())
print(game1.get_game_day())
print(gamesched)

#get tomorrow
