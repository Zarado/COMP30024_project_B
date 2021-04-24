from fire_punch.State import State
from fire_punch.Token import Token
from fire_punch.utils import find_legal_operations


class Player:
    # global constant

    maximum_tokens = 9

    # global variable

    turn = 0

    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        self.side = player
        self.enemy = 'NA'
        self.state = State()
        if player == 'upper':
            self.enemy = 'lower'
        else:
            self.enemy = 'upper'

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        print("input your action: ")
        action = input()
        if action == 'THROW':
            print("input your type: ")
            spe = input()
            print("input your destination: ")
            destination = tuple(eval(input()))
            action_list = (action, spe, destination)
        if action == 'SLIDE':
            print("input your hex: ")
            start = tuple(eval(input()))
            print("input your destination: ")
            destination = tuple(eval(input()))
            action_list = (action, start, destination)

        return action_list

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        self.operate(opponent_action, self.enemy)
        self.operate(player_action, self.side)
        self.battle(opponent_action[2])
        self.battle(player_action[2])
        # update the graph

    def battle(self, coordinate):
        battle_list = []
        for dict_val in self.state.upper_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type.lower() not in battle_list:
                        battle_list.append(token.type.lower())

        for dict_val in self.state.lower_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type not in battle_list:
                        battle_list.append(token.type.lower())

        if len(battle_list) == 3:
            self.state.remove_coordinate(coordinate, "all")

        if len(battle_list) == 2:

            if "r" in battle_list and "s" in battle_list:
                self.state.remove_coordinate(coordinate, "s")

            if "r" in battle_list and "p" in battle_list:
                self.state.remove_coordinate(coordinate, "r")

            if "p" in battle_list and "s" in battle_list:
                self.state.remove_coordinate(coordinate, "p")

    def operate(self, action, side):

        if action[0] == "THROW":
            if side == "lower":
                new_token = Token(action[2], action[1])
                self.state.lower_dict.get(new_token.type).append(new_token)
                self.state.throws_left[0] -= 1
            if side == "upper":
                new_token = Token(action[2], action[1].upper())
                self.state.upper_dict.get(new_token.type).append(new_token)
                self.state.throws_left[1] -= 1

        elif action[0] == "SLIDE" or "SWING":

            if side == "lower":
                for token in self.state.lower_dict["s"] + self.state.lower_dict["r"] + self.state.lower_dict["p"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)

            if side == "upper":
                for token in self.state.upper_dict["S"] + self.state.upper_dict["R"] + self.state.upper_dict["P"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)


player = Player("upper")
player.operate(("THROW", "s", (-3, 0)), "lower")
print(player.state.lower_dict)
print("--------")
print(find_legal_operations(player.state, 0))
print("----end----")
