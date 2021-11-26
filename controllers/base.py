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

    def make_matches(self, players):
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

    def tournament_menu_controller(self):
        next_round = False
        answer = input()
        if answer == "1":
            self.view.show_match_list(self.tournament.current_swiss_round)
        elif answer == "2":
            self.view.report_winner(self.tournament.current_swiss_round.matches)
        elif answer == "3":
            self.view.show_player_list(self.tournament.players)
        elif answer == "next":
            next_round = True
            self.tournament.swiss_round.append(self.tournament.current_swiss_round)
        return next_round

    def tournament_end_controller(self):
        program_end = False
        answer = input()
        if answer == "1":
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            round_number = self.view.ask_round_number(int(self.tournament.round_number))
            if round_number is not None:
                self.view.show_match_list(self.tournament.swiss_round[round_number])
        elif answer == "exit":
            program_end = True
        return program_end

    def run(self):
        running = True
        starting_menu = True
        program_end = False
        while running:
            while starting_menu:
                self.view.display_starting_menu()
                starting_menu = self.starting_menu_controller()
            for rounds in range(1, self.tournament.round_number+1):
                next_round = False
                self.update_points(self.tournament.players)
                self.make_matches(self.tournament.players)
                print("tour n"+str(rounds))
                while not next_round:
                    self.view.display_tournament_menu()
                    next_round = self.tournament_menu_controller()
            while not program_end:
                self.view.display_tournament_end()
                program_end = self.tournament_end_controller()
            running = False


controller = Controllers()
controller.run()
