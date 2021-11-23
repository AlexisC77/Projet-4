class Player:
    def __init__(self, name, age, points=0, elo=0):
        self.name = name
        self.age = age
        self.player_encounter = []
        self.matches = []
        self.points = points
        self.elo = elo

    def has_same_name(self, player1):
        if player1.name == self.name:
            test = True
        else:
            test = False
        return test


class Tournament:
    def __init__(self, date, round_number=4):
        self.date = date
        self.players = []
        self.round_number = round_number


class Match:
    def __init__(self, white_player, black_player, winner=None, score=None):
        self.white_player = white_player
        self.black_player = black_player
        self.winner = winner
        self.score = score


class SwissRound:
    def __init__(self):
        self.players = []
