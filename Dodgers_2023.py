import statsapi
import datetime
from tkinter import *
from PIL import ImageTk, Image
from datetime import timedelta, datetime, date



teams_list = []
teams_dict = {}
game_list = []
team = "Cubs"  # input("Enter a team: ")
live_stats = {}
game_dict = {}
base_runners = []
# if game is not active:
# show Next Game:
# away_team @ home_team
# date & time of game(PST)
# MoneyLine??? https://statsapi.mlb.com/api/{ver}/game/{gamePk}/winProbability

# if game is active:
# Inning & Top/Bottom arrow
# score
# now batting
    # Balls / Strikes
# now pitching
    # pitch count

# if game is over:
# Final Score
# Next Game info at bottom - After midnight, change to if game is not active display


class Team:
    """
    represents a MLB baseball Team
    Example:
    "id": 119,
    "name": "Los Angeles Dodgers",
    "teamCode": "lan",
    "fileCode": "la",
    "teamName": "Dodgers",
    "locationName": "Los Angeles",
    "shortName": "LA Dodgers"
    """
    def __init__(self, id, full_name, team_code, team_name, location, short_name):
        self._id = id
        self._full_name = full_name
        self._team_code = team_code
        self._team_name = team_name
        self._location = location
        self._short_name = short_name

    def get_id(self):
        return self._id

    def get_full_name(self):
        return self._full_name

    def get_team_name(self):
        return self._team_name


# print(statsapi.schedule(start_date=str(datetime.date.today()), end_date=str(datetime.date.today()+timedelta(days=7))))

# print(statsapi.lookup_team(''))

def build_teams(team):
    """builds dictionary of teams for creation of Team objects"""

    for teams in statsapi.lookup_team(''):
        team_name = teams["teamName"].replace(" ", "")
        this_team = dict()
        this_team["id"] = teams["id"]
        this_team["name"] = teams["name"]
        this_team["teamCode"] = teams["teamCode"]
        this_team["teamName"] = teams["teamName"]
        this_team["locationName"] = teams["locationName"]
        this_team["shortName"] = teams["shortName"]
        teams_dict[team_name] = this_team
        teams_list.append(this_team)
        # teams["teamCode"] = Team(teams["id"],teams["name"],teams["teamCode"],teams["fileCode"],teams["teamName"],teams["locationName"],teams["shortName"])

    team = Team(teams_dict[team]['id'], ['name'], ['teamCode'], ['teamName'], ['locationName'], ['shortName'])
    for game in statsapi.schedule(start_date=str(date.today()), end_date=str(date.today()+timedelta(days=3))):
        if game['away_id'] == team.get_id() or game['home_id'] == team.get_id():
            game_list.append(game)


class Game:
    """
    Represents a game between two MLB teams
    """
    def __init__(self, game_id, game_datetime, status, away_team, home_team, away_score, home_score, current_inning, inning_state, home_pitcher, away_pitcher):
        """
        Initializes a game object
        """
        self._game_id = game_id
        self._game_datetime = game_datetime
        self._status = status
        self._away_team = away_team
        self._home_team = home_team
        self._away_score = away_score
        self._home_score = home_score
        self._current_inning = current_inning
        self._inning_state = inning_state
        self._home_pitcher = home_pitcher
        self._away_pitcher = away_pitcher

    def get_live_stats(self):
        """
        Returns the live stats of a game
        """
        def get_baserunners(dict):
            """
            Returns the active base runners
            """
            if "first" in dict['offense']:
                base_runners.append(1)
            if "second" in dict['offense']:
                base_runners.append(2)
            if "third" in dict['offense']:
                base_runners.append(3)
            else:
                base_runners.append('')

        stats_dict = statsapi.get('game', {'gamePk': game_list[0]['game_id']})['liveData']['linescore']

        live_stats[self._away_team] = self.get_away_score()
        live_stats[self._home_team] = self.get_home_score()
        live_stats['now_pitching'] = self.get_pitcher(stats_dict)
        live_stats['now_batting'] = self.get_batter(stats_dict)
        live_stats['Inning'] = self._current_inning
        live_stats['inning_state'] = self.get_inning_state(stats_dict)
        live_stats['Bases'] = get_baserunners(stats_dict)
        live_stats['outs'] = stats_dict['outs']
        live_stats['balls'] = stats_dict['balls']
        live_stats['strikes'] = stats_dict['strikes']

    def get_inning_state(self, dict):
        """
        Returns top or bottom of inning as apppropriate
        """
        try:
            return dict['inningState']
        except KeyError:
            return "TBD"


    def get_pitcher(self, dict):
        """
        Returns current pitcher in game
        """
        try:
            return dict['defense']['pitcher']['fullName']
        except KeyError:
            return "TBD"

    def get_batter(self, dict):
        """
        Returns current batter
        """
        try:
            return dict['offense']['batter']['fullName']
        except KeyError:
            return "TBD"

    def get_inning(self):
        """
        Returns current Inning of game
        """
        return self._current_inning

    def get_home_score(self):
        """
        Returns the score the home team
        """
        return self._home_score

    def get_away_score(self):
        """
        Returns the score the away team
        """
        return self._away_score

    def get_home_team(self):
        """
        Returns the Home Team of a game
        """
        return self._home_team

    def get_away_team(self):
        """
        Returns the Away Team of a game
        """
        return self._away_team

    def get_id(self):
        """
        Returns the id of a Game
        """
        return self._game_id

    def get_home_pitcher(self):
        """
        Returns the starting pitcher for the Home team
        """
        return self._home_pitcher

    def get_away_pitcher(self):
        """
        Returns the starting pitcher for the Home team
        """
        return self._away_pitcher

    def retrieve_game_time(self):
        """
        returns the time of the next (in PST)
        """
        date_time = statsapi.get('game',{'gamePk': self.get_id()})['gameData']['datetime']['dateTime']
        time = date_time.split("T")[1].split("Z")[0]
        game_time = datetime.strptime(time, "%H:%M:%S")- timedelta(hours=7)
        return game_time.strftime('%I:%M %p')

    def retrieve_game_date(self):
        """
        returns the date of the next (in PST)
        """
        date_time_str = statsapi.get('game',{'gamePk': self.get_id()})['gameData']['datetime']['dateTime']
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
        game_date = date_time_obj.date()
        game_time = date_time_obj.time()
        if game_time.hour < 7:
            game_date -= timedelta(days=1)
            return game_date.strftime("%m/%d/%Y")
        else:
            return game_date.strftime("%m/%d/%Y")





def get_next_game():
    """
    Returns details of Next Game
    """
    game_dict["game_date"] = game_0.retrieve_game_date()
    game_dict["game_time"] = game_0.retrieve_game_time()
    game_dict["home_team"] = game_0.get_home_team()
    game_dict["home_pitcher"] = game_0.get_home_pitcher()
    game_dict["away_team"] = game_0.get_away_team()
    game_dict["away_pitcher"] = game_0.get_away_pitcher()
    return game_dict




build_teams(team)
game_0 = Game(game_list[0]['game_id'], game_list[0]['game_datetime'], game_list[0]['status'], game_list[0]['away_name'], game_list[0]['home_name'], game_list[0]['away_score'], game_list[0]['home_score'], game_list[0]['current_inning'],game_list[0]['inning_state'], game_list[0]['home_probable_pitcher'], game_list[0]['away_probable_pitcher'])


'''
# create root window
root = Tk()

# root window title and dimension
root.title("Dodgers Box Scores")
# Set geometry(widthxheight)
root.geometry('800x480')


away_team_logo = Label()

# Create a photoimage object of the image in the path
away_team = Image.open("logos\\" + game_list[0]['away_name'] + '.png')
away_team_res = away_team.resize((300,300))
away_team_pic = ImageTk.PhotoImage(away_team_res)
away_team_logo = Label(image=away_team_pic)
away_team_logo.image = away_team_pic
# Position image
away_team_logo.grid(column=0, row=0)
away_team_text = Label(root, text=game_list[0]['away_name'])
away_team_text.grid(column = 0, row = 1)

# At Text
at_text = Label(root, text="AT",width =int(20))
at_text.grid(column = 1, row = 0,sticky='nesw')


# Create a photoimage object of the image in the path
home_team = Image.open("logos\\" + game_list[0]['home_name'] + '.png')
home_team_res = home_team.resize((300,300))
home_team_pic = ImageTk.PhotoImage(home_team_res)
home_team_logo = Label(image=home_team_pic)
home_team_logo.image = away_team_pic
# Position image
home_team_logo.grid(row=0, column=3, sticky='e')
home_team_text = Label(root, text=game_list[0]['home_name'])
home_team_text.grid(column =3, row = 1)


# Execute Tkinter
root.mainloop()
'''

def pregame():
    """
    Launches the pregame screen
    """
    # screen layout
    root = Tk()
    root.geometry("800x480")
    root.maxsize(800,480)
    root.config(bg="DodgerBlue2")
    root.columnconfigure(1, weight=1)


    # away team logo
    away_team = Image.open("logos\\" + game_list[0]['away_name'] + '.png')
    away_team_resize = away_team.resize((250,250))
    away_team_pic = ImageTk.PhotoImage(away_team_resize)
    away_team_logo = Label(image=away_team_pic)
    away_team_logo.image = away_team_pic

    # AT
    at_text = Label(root, text="@", width=200, bg='DodgerBlue2', fg='white', font=('Ariel',100) )
    at_text.grid(column=1, row=0, sticky='nesw')

    #home team logo
    home_team = Image.open("logos\\" + game_list[0]['home_name'] + '.png')
    home_team_resize = home_team.resize((250,250))
    home_team_pic = ImageTk.PhotoImage(home_team_resize)
    home_team_logo = Label(image=home_team_pic)
    home_team_logo.image = home_team_pic

    # Next Game Date
    game_date_text = Label(root, text="Next Game: ", bg='DodgerBlue2', fg='white', font=('Ariel'))
    game_date_text.grid(column=1, row=1, sticky='we')
    game_date_date = Label(root, text = game_0.retrieve_game_date() + ", " +game_0.retrieve_game_time(),bg='DodgerBlue2', fg='white', font=('Ariel'))
    game_date_date.grid(column=1, row=2, sticky='we')

    # Next Pitcher Data
    away_pitcher_text = Label(root,text="Starting Pitcher:",bg='DodgerBlue2', fg='white', font=('Ariel'))
    away_pitcher_text.grid(column=0, row=1, sticky='w')
    away_pitcher_pitcher = Label(root,text=game_0.get_away_pitcher(),bg='DodgerBlue2', fg='white', font=('Ariel'))
    away_pitcher_pitcher.grid(column=0,row=2,sticky='sw')

    home_pitcher_text = Label(root,text="Starting Pitcher:",bg='DodgerBlue2', fg='white', font=('Ariel'))
    home_pitcher_text.grid(column=2, row=1, sticky='w')
    home_pitcher_pitcher = Label(root,text=game_0.get_home_pitcher(),bg='DodgerBlue2', fg='white', font=('Ariel'))
    home_pitcher_pitcher.grid(column=2,row=2,sticky='sw')

    # Next Game Time
    # game_time = Label(root, text=game_0.retrieve_game_time(), bg='DodgerBlue2', fg='white', font=('Ariel'))
    # game_time.grid(column=1, row=2, sticky='w')
    # Position images
    away_team_logo.grid(column=0, row=0)
    home_team_logo.grid(column=2, row=0)
    #away_team_logo.grid(column=0, row=0)
    root.mainloop()


def game():
    """
    Launches the live game screen
    """
    # screen layout
    root = Tk()
    root.geometry("800x480")
    root.maxsize(800,480)
    root.config(bg="DodgerBlue2")
    root.columnconfigure(1, weight=1)

    # away team logo
    away_team = Image.open("logos\\" + game_list[0]['away_name'] + '.png')
    away_team_resize = away_team.resize((100,100))
    away_team_pic = ImageTk.PhotoImage(away_team_resize)
    away_team_logo = Label(image=away_team_pic, bg='DodgerBlue2')
    away_team_logo.image = away_team_pic

    # BaseRunners
    print(base_runners)
    if 1 in base_runners:
        if 2 in base_runners:
            if 3 in base_runners:
                base_status = "1-2-3"
            else:
                base_status = "1-2"
        else:
            if 3 in base_runners:
                base_status = "1-3"
            else:
                base_status = "1"
    elif 2 in base_runners:
        if 3 in base_runners:
            base_status = "2-3"
        else:
            base_status = "2"
    elif 3 in base_runners:
        base_status = "3"
    else:
        base_status = "Empty"
    baserunners_base = Image.open("baserunners\\" + base_status + ".png")
    baserunners_resize = baserunners_base.resize((250,250))
    baserunners_pic = ImageTk.PhotoImage(baserunners_resize)
    baserunners = Label(image=baserunners_pic, bg='DodgerBlue2')

    #home team logo
    home_team = Image.open("logos\\" + game_list[0]['home_name'] + '.png')
    home_team_resize = home_team.resize((100,100))
    home_team_pic = ImageTk.PhotoImage(home_team_resize)
    home_team_logo = Label(image=home_team_pic, bg='DodgerBlue2')
    home_team_logo.image = home_team_pic
    away_team_logo.grid(column=0, row=0)
    home_team_logo.grid(column=2, row=0)
    baserunners.grid(column=1, row=0, sticky='new')
    root.mainloop()


if datetime.today()+timedelta(hours=7) < datetime.strptime(game_list[0]['game_datetime'], "%Y-%m-%dT%H:%M:%SZ"):
    pregame()
else:

    game_0.get_live_stats()
    game()
    print(live_stats)
    print(base_runners)


