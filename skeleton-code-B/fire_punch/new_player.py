import sys

sys.path.append('..')

from fire_punch.State import State
from fire_punch.Token import Token
from fire_punch.utils import find_legal_operations
from fire_punch.utils import evaluation
from fire_punch.utils import compute_matrix
from fire_punch.utils import get_expected_value
from fire_punch.utils import estimate_evaluation
from fire_punch.utils import new_turn
from fire_punch.utils import find_abitary_move

import numpy as np

import copy


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
        self.enemy = -1
        self.side = -1
        self.upper_dict = {"R": [], "P": [], "S": []}
        self.lower_dict = {"r": [], "p": [], "s": []}
        self.throws_left = [9, 9]
        self.token_left = [0, 0]
        if player == 'upper':
            self.side = 1
            self.enemy = 0
        else:
            self.side = 0
            self.enemy = 1


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        """
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
        """

        # move = alpha_beta_minimax(self.state, 2, True, self.side, float('-inf'), float('inf'))[1]

        return 0

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

    def operate(self, action, side):
        if action[0] == "THROW":
            if side == 0:
                new_token = [action[2], action[1].lower]
                self.lower_dict.get(new_token[1]).append(new_token)
                self.throws_left[0] -= 1
                self.token_left[0] += 1
            if side == 1:
                new_token = [action[2], action[1].upper()]
                self.upper_dict.get(new_token[1]).append(new_token)
                self.throws_left[1] -= 1
                self.token_left[1] += 1

        elif action[0] == "SLIDE" or "SWING":

            if side == 0:
                for token in self.lower_dict["s"] + self.lower_dict["r"] + self.lower_dict["p"]:
                    if token[0] == action[1]:
                        token[0] = action[2]
                        break

            if side == 1:
                for token in self.upper_dict["S"] + self.upper_dict["R"] + self.upper_dict["P"]:
                    if token[0] == action[1]:
                        token[0] = action[2]
                        break

    def battle(self, coordinate):
        battle_list = []
        for dict_val in self.upper_dict.values():
            for token in dict_val:
                if token[0] == coordinate:
                    if token[1].lower() not in battle_list:
                        battle_list.append(token[1].lower())

        for dict_val in self.lower_dict.values():
            for token in dict_val:
                if token[0] == coordinate:
                    if token[1].lower() not in battle_list:
                        battle_list.append(token[1].lower())

        if len(battle_list) == 3:
            self.remove_coordinate(coordinate, "all")

        if len(battle_list) == 2:

            if "r" in battle_list and "s" in battle_list:
                self.remove_coordinate(coordinate, "s")

            if "r" in battle_list and "p" in battle_list:
                self.remove_coordinate(coordinate, "r")

            if "p" in battle_list and "s" in battle_list:
                self.remove_coordinate(coordinate, "p")


    def remove_coordinate(self, coordinate, spices):
        if spices == "all":
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token[0] == coordinate:
                        self.upper_dict.get(key).remove(token)
                        self.token_left[1] -= 1

            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token[0] == coordinate:
                        self.lower_dict.get(key).remove(token)
                        self.token_left[0] -= 1
        else:
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token[0] == coordinate and token[1] == spices.upper():
                        self.upper_dict.get(key).remove(token)
                        self.token_left[1] -= 1

            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token[0] == coordinate and token[1] == spices.lower():
                        self.lower_dict.get(key).remove(token)
                        self.token_left[0] -= 1