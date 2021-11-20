class Player:
    def __init__(self, name, age, elo=0):
        self.name = name
        self.age = age
        self.player_encounter = []
        self.elo = elo

    def show_player(self):
        if self.elo <= 0:
            print(self.name + " is " + str(self.age) + " years old, his elo is indeterminate")
        else:
            print(self.name + " is " + str(self.age) + "years old, his elo is " + str(self.elo))


class Tournament:
    def __init__(self, date, round_number):
        self.date = date
        self.players = []
        self.round_number = round_number


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


class SwissRound:
    def __init__(self):
        self.players = []


player_test = Player(name="Alexis", age=20, elo=1100)
player_test.show_player()
