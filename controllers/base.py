from views.base import View

from models.base import Player
from models.base import Tournament

player_test = Player(name="Alexis", age=20, elo=1200)


class Controllers:

    def __init__(self):
        self.view = View()
        self.tournament = Tournament("date")

    def update_points(self, players):
        pass

    def start_tournament(self):
        pass

    def starting_menu_controller(self):
        answer = input()
        starting_menu = True
        if answer == "1":
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            self.view.add_player(self.tournament.players)
        elif answer == "3":
            self.view.remove_player(self.tournament.players)
        elif answer == "4":
            self.view.change_round_number(self.tournament)
        elif answer == "go":
            self.start_tournament()
            starting_menu = False
        return starting_menu

    def run(self):
        running = True
        starting_menu = True
        while running:
            while starting_menu:
                self.view.display_starting_menu()
                starting_menu = self.starting_menu_controller()
            running = False


controller = Controllers()
controller.run()
