from tinydb import TinyDB
import time


class Player:
    def __init__(self, first_name, last_name, birth_date, gender, matches=None,
                 player_encounter=None, points=0, elo=0):
        if player_encounter is None:
            player_encounter = []
        if matches is None:
            matches = []
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.matches = matches
        self.player_encounter = player_encounter
        self.points = points
        self.elo = elo

    def serialized(self):
        player_encounter_list = []
        matches_list = []
        for player in self.player_encounter:
            player_encounter = {'first name': player.first_name, 'last name': player.last_name,
                                'birth date': player.birth_date,
                                "gender": player.gender, "points": player.points, "elo": player.elo}
            player_encounter_list.append(player_encounter)
            for match in player.matches:
                matches_list.append(match.serialized())
        serialized_player = {'first name': self.first_name, 'last name': self.last_name, 'birth date': self.birth_date,
                             "gender": self.gender, "matches": matches_list, "player encounter": player_encounter_list,
                             "points": self.points, "elo": self.elo}
        return serialized_player

    def has_same_name(self, player1):
        if player1.first_name == self.first_name and player1.last_name == self.last_name:
            test = True
        else:
            test = False
        return test


def deserialized_player(serialized_player):
    if serialized_player is None:
        return None
    else:
        player_encounter_list = []
        matches_list = []
        for match in serialized_player["matches"]:
            matches_list.append(deserialized_match(match))
        for player in serialized_player["player encounter"]:
            player_encounter_list.append(
                Player(player["first name"], player["last name"], player["birth date"], player["gender"], matches=[],
                       player_encounter=[], points=player["points"], elo=player["elo"]))
        return Player(serialized_player["first name"], serialized_player["last name"], serialized_player["birth date"],
                      serialized_player["gender"], matches=matches_list, player_encounter=player_encounter_list,
                      points=serialized_player["points"], elo=serialized_player["elo"])


class Tournament:
    def __init__(self, name, place, description, time_control, round_number=4, date=time.strftime('%d/%m/%Y'),
                 players=None, swiss_round=None, current_swiss_round_number=1):
        if swiss_round is None:
            swiss_round = []
        if players is None:
            players = []
        self.name = name
        self.place = place
        self.description = description
        self.time_control = time_control
        self.round_number = round_number
        self.date = date
        self.players = players
        self.tournament_table = TinyDB("tournament.json")
        self.swiss_round = swiss_round
        self.current_swiss_round_number = current_swiss_round_number

    def serialized(self):
        player_list = []
        for player in self.players:
            player_list.append(player.serialized())
        swiss_round_list = []
        for swiss_round in self.swiss_round:
            swiss_round_list.append(swiss_round.serialized())
        serialized_tournament = {'date': self.date, 'name': self.name, 'place': self.place,
                                 'description': self.description, 'time control': self.time_control,
                                 'round number': self.round_number, 'players': player_list,
                                 'swiss round': swiss_round_list,
                                 'current swiss round number': self.current_swiss_round_number}
        return serialized_tournament

    def sort_by_elo(self):
        sorted_players = []
        while self.players:
            upper = self.players[0].elo
            upper_index = 0
            current_index = 0
            for player in self.players:
                if upper < player.elo:
                    upper = player.elo
                    upper_index = current_index
                current_index += 1
            sorted_players.append(self.players.pop(upper_index))
        self.players = sorted_players

    def sort_by_points(self):
        sorted_players = []
        while self.players:
            upper = self.players[0].points
            upper_index = 0
            current_index = 0
            for player in self.players:
                if upper < player.points:
                    upper = player.points
                    upper_index = current_index
                current_index += 1
            sorted_players.append(self.players.pop(upper_index))
        self.players = sorted_players

    def sort_by_name(self):
        sorted_players = []
        while self.players:
            upper = self.players[0].first_name + " " + self.players[0].last_name
            upper_index = 0
            current_index = 0
            for player in self.players:
                if upper.capitalize() > player.first_name + " " + player.last_name.capitalize():
                    upper = player.first_name + " " + player.last_name
                    upper_index = current_index
                current_index += 1
            sorted_players.append(self.players.pop(upper_index))
        self.players = sorted_players


class Match:
    def __init__(self, first_player, second_player, winner=None):
        self.first_player = first_player
        self.second_player = second_player
        self.winner = winner

    def serialized(self):
        if self.first_player:
            first_player = {"first name": self.first_player.first_name, "last name": self.first_player.last_name,
                            "birth date": self.first_player.birth_date, "gender": self.first_player.gender,
                            "matches": [], "player encounter": [], "points": self.first_player.points,
                            "elo": self.first_player.elo}
        else:
            first_player = None
        if self.second_player:
            second_player = {"first name": self.second_player.first_name, "last name": self.second_player.last_name,
                             "birth date": self.second_player.birth_date, "gender": self.second_player.gender,
                             "matches": [], "player encounter": [], "points": self.second_player.points,
                             "elo": self.second_player.elo}
        else:
            second_player = None
        if self.winner:
            winner = {"first name": self.winner.first_name, "last name": self.winner.last_name,
                      "birth date": self.winner.birth_date, "gender": self.winner.gender, "matches": [],
                      "player encounter": [], "points": self.winner.points,
                      "elo": self.winner.elo}
        else:
            winner = None
        serialized_match = {"first player": first_player, "second player": second_player, "winner": winner}
        return serialized_match


def deserialized_match(serialized_match):
    player1 = deserialized_player(serialized_match["first player"])
    player2 = deserialized_player(serialized_match["second player"])
    winner = deserialized_player(serialized_match["winner"])
    return Match(player1, player2, winner)


class SwissRound:
    def __init__(self, swiss_round_number, matches=None, date=time.strftime('%d/%m/%Y'),
                 starting_hour=time.strftime('%H:%M', time.localtime()), ending_hour="indeterminate"):
        if matches is None:
            matches = []
        self.swiss_round_number = swiss_round_number
        self.matches = matches
        self.date = date
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour

    def serialized(self):
        match_list = []
        for match in self.matches:
            match_list.append(match.serialized())
        serialized_swiss_round = {"round number": self.swiss_round_number, "match list": match_list, "date": self.date,
                                  "starting hour": self.starting_hour, "ending hour": self.ending_hour}
        return serialized_swiss_round
