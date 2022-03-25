from views.base import View
from models.base import Player
from models.base import Match
from models.base import SwissRound
from models.base import Tournament
from models.base import deserialized_player
from models.base import deserialized_match
import time
from tinydb import TinyDB


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

    def make_matches_first_round(self):
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
            self.tournament.swiss_round[-1].matches.append(Match(player1, player2))
            player1.matches.append(self.tournament.swiss_round[-1].matches[-1])
            player2.matches.append(self.tournament.swiss_round[-1].matches[-1])
            player1.player_encounter.append(player2)
            player2.player_encounter.append(player1)
        if len(not_choose_players_down) == 1:
            free_win = Player("free", "win", "00/00/0000", "other")
            self.tournament.swiss_round[-1].matches.append(not_choose_players_down[0], free_win)
            self.tournament.swiss_round[-1].player_encounter.append(free_win)
            self.tournament.swiss_round[-1].matches[-1].winner = self.tournament.swiss_round[-1].matches[-1][0][0]
            self.tournament.swiss_round[-1].matches[-1][1] = "victoire"

    def make_matches_other_round(self):
        self.tournament.sort_by_points()
        not_choose_players = []
        for player in self.tournament.players:
            not_choose_players.append(player)
        while len(not_choose_players) > 1:
            player1 = not_choose_players.pop(0)
            test = False
            index = 0
            while not test:
                if not_choose_players[index] not in player1.player_encounter:
                    player2 = not_choose_players.pop(index)
                    self.tournament.swiss_round[-1].matches.append(Match(player1, player2))
                    player1.matches.append(self.tournament.swiss_round[-1].matches[-1])
                    player2.matches.append(self.tournament.swiss_round[-1].matches[-1])
                    player1.player_encounter.append(player2)
                    player2.player_encounter.append(player1)
                    test = True
                elif index < len(not_choose_players)-1:
                    index += 1
                else:
                    player2 = not_choose_players.pop(0)
                    self.tournament.swiss_round[-1].matches.append(Match(player1, player2))
                    player1.matches.append(self.tournament.swiss_round[-1].matches[-1])
                    player2.matches.append(self.tournament.swiss_round[-1].matches[-1])
                    player1.player_encounter.append(player2)
                    player2.player_encounter.append(player1)
                    test = True

    def start_tournament(self):
        self.update_database()
        self.tournament.swiss_round.append(SwissRound(1))

    def update_database(self):
        self.tournament.tournament_table.table('current_tournament').truncate()
        self.tournament.tournament_table.table('current_tournament').insert(self.tournament.serialized())
        for player in self.tournament.players:
            already_in_base = False
            for player_from_table in TinyDB("player.json").table('player_list'):
                if player.first_name+player.last_name == player_from_table["first name"] + \
                        player_from_table["last name"]:
                    already_in_base = True
            if not already_in_base:
                TinyDB("player.json").table('player_list').insert(player.serialized())

    def update_tournament(self):
        tournaments_table = TinyDB("tournament.json").table("current_tournament")
        for tournament in tournaments_table:
            serialised_player_list = tournament['players']
            player_list = []
            for player in serialised_player_list:
                player_list.append(deserialized_player(player))
            self.tournament = Tournament(tournament['name'], tournament['place'],
                                         tournament['description'], tournament['time control'],
                                         tournament['round number'], tournament["date"],
                                         player_list, tournament['swiss round'],
                                         tournament['current swiss round number'])

    def starting_menu_controller(self):
        answer = input()
        player_list = []
        serialised_player_list = TinyDB("player.json").table('player_list')
        for player in serialised_player_list:
            player_list.append(deserialized_player(player))
        database_tournament = Tournament("name", "place", "description", "time control", players=player_list)
        starting_menu = True
        if answer == "1":
            self.tournament.sort_by_name()
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            self.tournament.players = self.view.add_player(self.tournament.players)
        elif answer == "3":
            self.view.remove_player(self.tournament.players)
        elif answer == "4":
            self.view.change_round_number(self.tournament)
        elif answer == "5":
            database_tournament.sort_by_name()
            self.view.show_player_list(database_tournament.players)
        elif answer == "6":
            database_tournament.sort_by_elo()
            self.view.show_player_list(database_tournament.players)
        elif answer == "7":
            self.tournament.players = self.view.add_player_from_database(database_tournament, self.tournament.players)
        elif answer == "8":
            self.past_tournament_controller()
        elif answer == "update":
            self.update_database()
        elif answer == "import":
            self.update_tournament()
        elif answer == "go":
            self.start_tournament()
            starting_menu = False
        return starting_menu

    def past_tournament_controller(self):
        tournament_list = []
        tournaments_table = TinyDB("tournament.json").table("archived_tournament")
        for tournament in tournaments_table:
            player_list = []
            swiss_round_list = []
            for player in tournament['players']:
                player_list.append(deserialized_player(player))
            for information in tournament['swiss round']:
                swiss_round_match_list = []
                for match in information["match list"]:
                    swiss_round_match_list.append(deserialized_match(match))
                swiss_round_list.append(SwissRound(information["round number"], swiss_round_match_list,
                                                   information["date"], information["starting hour"],
                                                   information["ending hour"]))
            tournament = Tournament(tournament['name'], tournament['place'], tournament['description'],
                                    tournament['time control'],
                                    tournament['round number'], tournament["date"], player_list, swiss_round_list,
                                    tournament['current swiss round number'])
            tournament_list.append(tournament)
        exit_menu = False
        while not exit_menu:
            self.view.display_past_tournament()
            answer = input()
            if answer == "1":
                tournament_number = 1
                for tournament in tournament_list:
                    print(str(tournament_number) + "  " + tournament.date + "  " + tournament.name + "  " +
                          tournament.place)
                    print(tournament.description)
                    tournament_number += 1
            if answer == "2":
                exit_menu = True
            if answer == "3":
                tournament_number = self.view.ask_tournament_number(self.tournament.round_number)
                if tournament_number is not None:
                    self.see_tournament(tournament_list[tournament_number])

    def see_tournament(self, tournament):
        exit_menu = False
        while not exit_menu:
            self.view.explore_past_tournament()
            answer = input()
            if answer == "1":
                self.view.show_player_list(tournament.players)
            if answer == "2":
                for swiss_round in tournament.swiss_round:
                    print("round number ° " + str(swiss_round.swiss_round_number) + "made the : " + swiss_round.date +
                          "started at : " + swiss_round.starting_hour + "and end at : " + swiss_round.ending_hour)
            if answer == "3":
                for swiss_round in tournament.swiss_round:
                    print("")
                    self.view.show_match_list(swiss_round)
                    print("")
            if answer == "4":
                exit_menu = True

    def tournament_menu_controller(self):
        next_round = False
        answer = input()
        if answer == "4":
            self.view.show_match_list(self.tournament.swiss_round[-1])
        elif answer == "3":
            self.view.report_winner(self.tournament.swiss_round[-1].matches)
        elif answer == "2":
            self.tournament.sort_by_points()
            self.view.show_player_list(self.tournament.players)
        elif answer == "1":
            self.tournament.sort_by_name()
            self.view.show_player_list(self.tournament.players)
        elif answer == "update":
            self.update_database()
        elif answer == "next":
            self.next_round()
            next_round = True
        return next_round

    def next_round(self):
        self.tournament.swiss_round[-1].ending_hour = time.strftime('%H:%M', time.localtime())
        self.update_points()
        if self.tournament.current_swiss_round_number < self.tournament.round_number:
            self.tournament.current_swiss_round_number += 1
            self.tournament.swiss_round.append(SwissRound(self.tournament.current_swiss_round_number))

    def tournament_end_controller(self, saved_boolean):
        program_end = False
        answer = input()
        if answer == "1":
            self.tournament.sort_by_name()
            self.view.show_player_list(self.tournament.players)
        elif answer == "2":
            self.tournament.sort_by_points()
            self.view.show_player_list(self.tournament.players)
        elif answer == "3":
            round_number = self.view.ask_round_number(self.tournament.round_number)
            if round_number is not None:
                self.view.show_match_list(self.tournament.swiss_round[round_number])
        elif answer == "save" and not saved_boolean:
            self.tournament.tournament_table.table("archived_tournament").insert(self.tournament.serialized())
            saved_boolean = True
        elif answer == "save" and saved_boolean is True:
            print("you already saved this tournament")
        elif answer == "exit":
            program_end = True
        return [program_end, saved_boolean]

    def run(self):
        running = True
        starting_menu = True
        program_end = [False, False]
        while running:
            while starting_menu:
                self.view.display_starting_menu()
                starting_menu = self.starting_menu_controller()
            for rounds in range(self.tournament.current_swiss_round_number, int(self.tournament.round_number)+1):
                next_round = False
                if self.tournament.current_swiss_round_number == 1:
                    self.tournament.swiss_round[-1].starting_hour = time.strftime('%H:%M', time.localtime())
                    self.make_matches_first_round()
                else:
                    self.tournament.swiss_round[-1].starting_hour = time.strftime('%H:%M', time.localtime())
                    self.make_matches_other_round()
                while not next_round:
                    self.view.display_tournament_menu()
                    next_round = self.tournament_menu_controller()
            self.tournament.swiss_round[-1].ending_hour = time.strftime('%H:%M', time.localtime())
            while not program_end[0]:
                self.view.display_tournament_end()
                program_end = self.tournament_end_controller(program_end[1])
            running = False
