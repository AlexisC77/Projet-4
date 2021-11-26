from models.base import Player


class View:

    def input_player(self):
        print("Enter player's name:")
        name = input()
        print("Enter player's age:")
        age = input()
        print("Enter player's elo, enter 0 if you don't want to:")
        elo = input()
        return Player(name=name, age=age, elo=elo)

    def display_starting_menu(self):
        print()
        print("enter 1 to see the player list")
        print("enter 2 to add a player to the list")
        print("enter 3 to remove a player from the list")
        print("enter 4 to change the number of round of this tournament")
        print("enter \"go\" to launch the tournament, if you do It you will not be able to change the player list")
        print()

    def show_player_list(self, players):
        if len(players) == 0:
            print("player list is empty")
        number = 1
        for player in players:
            if not isinstance(player.elo, int) or player.elo <= 0:
                print(str(number) + "   " + player.name + " is " + str(
                    player.age) + " years old, his elo is indeterminate, he has "+str(player.points)+" points")
            else:
                print(str(number) + "   " + player.name + " is " + str(player.age) + " years old, his elo is " + str(
                    player.elo)+" he has "+str(player.points)+" points")
            number += 1

    def add_player(self, players):
        player = self.input_player()
        test = False
        for player_from_list in players:
            test = player.has_same_name(player_from_list)
        if not test:
            players.append(player)
            print("player has been successfully added to the tournament")
        else:
            print("a player is already named like this in the tournament, please retry with an other name")
        print("if you want to add another player enter \"y\" if not, enter anything else")
        restart = input()
        if restart == "y":
            View.add_player(self, players)
        return players

    def remove_player(self, players):
        if len(players) == 0:
            print("player list is empty")
        else:
            print("Enter player's number of the one you want to remove, press 0 if you don't want to remove a player")
            index = int(input())
            if index < 1 or index > len(players):
                print("number is not valid, It is write in the player list please check and retry")
            else:
                print("do you want to remove\" " + players[index - 1].name + "\" from this tournament?")
                print("press \"y\" for yes and anything else for no")
                confirm = input()
                if confirm == "y":
                    players.pop(index - 1)
                    print("player has been successfully removed from the tournament")
        return players

    def change_round_number(self, tournament):
        print("Enter the number of round that you want for this tournament, current number is: "+str(tournament.round_number))
        answer = input()
        if not is_number(answer):
            print("please choose an integer number, the value did not change")
        else:
            tournament.round_number = int(answer)
            print("the number of round has been changed to "+str(answer))

    def display_tournament_menu(self):
        print()
        print("Enter 1 if you want to see the match list")
        print("Enter 2 if you want to report the score of a match")
        print("enter 3 if you want to see the player list")
        print("Enter \"next\" if you want to go to the next round, unreported results will be considered as draw "
              "and you will not be able to go back to change results of this round")
        print()

    def show_match_list(self, swiss_round):
        if not swiss_round.matches:
            print("match list is empty")
        else:
            number = 1
            for match in swiss_round.matches:
                if match.winner is None:
                    print(str(number) + "    " + match.white_player + " vs " + match.black_player +
                          "     result still undetermined")
                else:
                    print(str(number) + "    " + match.white_player + " vs " + match.black_player +
                          "     the winner is :" + match.winner)
                number += 1

    def report_winner(self, matches):
        print("Enter the number of the match of which you want to report the result")
        index = input()
        if not is_number(index) or int(index) < 1 or int(index) >= len(matches):
            print("number is not valid, It is write in the matches list please check and retry")
        else:
            index = int(index)
            print("if \"" + matches[index].white_player + "\" won, enter 1, if \"" + matches[index].black_player +
                  "\" won, enter 2, if they made a draw enter 0, enter anything else to not update the result")
            result = input()
            if result not in ["0", "1", "2"]:
                print("you didn't enter 0, 1 or 2 so the result as not being updated")
            else:
                if result == "0":
                    matches[index].winner = None
                elif result == "1":
                    matches[index].winner = matches[index].white_player
                else:
                    matches[index].winner = matches[index].black_player
        print("if you want to add another result enter \"y\" if not, enter anything else")
        restart = input()
        if restart == "y":
            View.report_winner(self, matches)
        return matches

    def display_tournament_end(self):
        print("Enter 1 if you want to see the player List")
        print("Enter 2 if you want to see a match list of a particular round")
        print("Enter \"exit\" if you want to end this tournament, you will not be able to make any changes on It "
              "or to watch information from It after that")

    def ask_round_number(self, round_number):
        print(round_number)
        print("which round de you want to see?")
        answer = input()
        if not is_number(answer):
            print("this is not a number, please retry")
        elif int(answer) < 1 or int(answer) > round_number:
            print("retry and choose a valid number please")
        else:
            return int(answer)-1
        return None


def is_number(string):
    test = True
    if string is None or string == "":
        test = False
    elif string[0] == "-":
        string = string[1:]
    if test:
        for i in string:
            if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                test = False
    return test
