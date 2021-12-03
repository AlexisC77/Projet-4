from tinydb import TinyDB


class Player:
    def __init__(self, first_name, last_name, birth_date, gender, points=0, elo=0):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.player_encounter = []
        self.matches = []
        self.points = points
        self.elo = elo

    def serialized(self):
        serialized_player = {'first name': self.first_name, 'last name': self.last_name, 'birth date': self.birth_date,
                             "gender": self.gender, "points": self.points, "elo": self.elo}
        return serialized_player

    def has_same_name(self, player1):
        if player1.first_name == self.first_name and player1.last_name == self.last_name:
            test = True
        else:
            test = False
        return test


class Tournament:
    def __init__(self, date, name, place, description, time_control, round_number=4):
        self.date = date
        self.name = name
        self.place = place
        self.description = description
        self.time_control = time_control
        self.round_number = round_number
        self.players = []
        db = TinyDB("database.json")
        self.players_table = db.table("players")
        self.swiss_round = []
        self.current_swiss_round = SwissRound("date")
        self.current_swiss_round_number = 1

    def sort_by_elo(self):
        sorted_players = []
        while self.players:
            upper = self.players[0].elo
            upper_index = 0
            current_index = 0
            for player in self.players:
                if upper < player.elo:
                    upper = player.elo
                    print(upper)
                    upper_index = current_index
                current_index += 1
            sorted_players.append(self.players.pop(upper_index))
        self.players = sorted_players


class Match:
    def __init__(self, first_player, second_player, winner=None):
        self.first_player = []
        self.second_player = []
        self.first_player.append(first_player)
        self.first_player.append(None)
        self.second_player.append(second_player)
        self.second_player.append(None)
        self.winner = winner


class SwissRound:
    def __init__(self, date, starting_hour="start", ending_hour="end"):
        self.matches = []
        self.date = date
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour
