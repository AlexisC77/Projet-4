from views.base import View
from models.base import Player
from models.base import Match


class Controllers:

    def __init__(self, tournament):
        self.view = View()
        self.tournament = tournament

    def update_points(self):
        for player in self.tournament.players:
            if not player.matches[-1].winner:
                player.points += 0.5
            elif player.has_same_name(player.matches[-1].winner):
                player.points += 1

    def make_matches(self):
        if self.tournament.current_swiss_round_number == 1:
            self.tournament.sort_by_elo()
            not_choose_players_up = []
            not_choose_players_down = []
            number = 1
            for player in self.tournament.players:
                if number <= len(self.tournament.players)/2:
                    not_choose_players_up.append(player)
                else:
                    not_choose_players_down.append(player)
                number += 1
            while len(not_choose_players_up) + len(not_choose_players_down) > 1:
                player1 = not_choose_players_up.pop(0)
                player2 = not_choose_players_down.pop(0)
                self.tournament.current_swiss_round.matches.append(Match(player1, player2))
                player1.matches.append(Match(player1, player2))
                player2.matches.append(Match(player1, player2))
            if len(not_choose_players_down) == 1:
                free_win = Player("free", "win", "00/00/0000", "other")
                self.tournament.current_swiss_round.matches.append(not_choose_players_down[0], free_win)
                self.tournament.current_swiss_round.matches[-1].winner = self.tournament.current_swiss_round.matches[-1][0][0]
                self.tournament.current_swiss_round.matches[-1][1] = "victoire"
        else:
            pass

    def start_tournament(self):
        self.update_database(self.tournament.players_table)

    def update_database(self, players_table):
        serialized_players = []
        for player in self.tournament.players:
            serialized_players.append(player.serialized())
        players_table.truncate()
        players_table.insert_multiple(serialized_players)

    def update_player_list(self):
        deserialized_players = []
        for player in self.tournament.players_table:
            deserialized_players.append(Player(player["first name"], player["last name"], player["birth date"],
                                               player["gender"], player["points"], player["elo"]))
        self.tournament.players = deserialized_players

    def starting_menu_controller(self):
        answer = input()
        starting_menu = True
        if answer == "1":
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            self.tournament.players = self.view.add_player(self.tournament.players)
        elif answer == "3":
            self.view.remove_player(self.tournament.players)
        elif answer == "4":
            self.view.change_round_number(self.tournament)
        elif answer == "update":
            self.update_database(self.tournament.players_table)
        elif answer == "import":
            self.update_player_list()
        elif answer == "go":
            self.start_tournament()
            starting_menu = False
        return starting_menu

    def tournament_menu_controller(self):
        next_round = False
        answer = input()
        if answer == "3":
            self.view.show_match_list(self.tournament.current_swiss_round)
        elif answer == "2":
            self.view.report_winner(self.tournament.current_swiss_round.matches)
        elif answer == "1":
            self.view.show_player_list(self.tournament.players)
        elif answer == "update":
            self.update_database(self.tournament.players_table)
        elif answer == "next":
            next_round = True
            self.tournament.swiss_round.append(self.tournament.current_swiss_round)
            self.tournament.current_swiss_round_number += 1
        return next_round

    def tournament_end_controller(self):
        program_end = False
        answer = input()
        if answer == "1":
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            round_number = self.view.ask_round_number("they were "+str(self.tournament.round_number) + " rounds in this tournament")
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
                self.make_matches()
                while not next_round:
                    self.view.display_tournament_menu()
                    next_round = self.tournament_menu_controller()
                self.update_points()
            while not program_end:
                self.view.display_tournament_end()
                program_end = self.tournament_end_controller()
            running = False
