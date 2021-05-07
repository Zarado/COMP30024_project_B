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
        self.state = [{"r": [], "p": [], "s": []}, {"R": [], "P": [], "S": []}, [9, 9], [0, 0]]
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
                new_token = [action[2], action[1].lower()]
                self.state[0].get(new_token[1]).append(new_token)
                self.state[2][0] -= 1
                self.state[3][0] += 1
            if side == 1:
                new_token = [action[2], action[1].upper()]
                self.state[1].get(new_token[1]).append(new_token)
                self.state[2][1] -= 1
                self.state[3][1] += 1

        elif action[0] == "SLIDE" or "SWING":

            if side == 0:
                for action in self.state[0].values():
                    for token in action:
                        if token[0] == action[1]:
                            token[0] = action[2]
                            break

            if side == 1:
                for action in self.state[1].values():
                    for token in action:
                        if token[0] == action[1]:
                            token[0] = action[2]
                            break

    def battle(self, coordinate):

        battle_list = []

        for action in self.state[0].values():
            for token in action:
                if token[0] == coordinate:
                    if token[1].lower() not in battle_list:
                        battle_list.append(token[1].lower())

        for action in self.state[1].values():
            for token in action:
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

            for action in self.state[0].values():
                for token in action:
                    if token[0] == coordinate:
                        self.state[0].get(token[1]).remove(token)
                        self.state[3][0] -= 1

            for action in self.state[1].values():
                for token in action:
                    if token[0] == coordinate:
                        self.state[1].get(token[1]).remove(token)
                        self.state[3][1] -= 1

        else:

            for action in self.state[0].values():
                for token in action:
                    if token[0] == coordinate and token[1] == spices.lower():
                        self.state[0].get(token[1]).remove(token)
                        self.state[3][0] -= 1

            for action in self.state[1].values():
                for token in action:
                    if token[0] == coordinate and token[1] == spices.upper():
                        self.state[1].get(token[1]).remove(token)
                        self.state[3][1] -= 1


def simulation(state, side, move, ismax):
    moves = []
    after_move = []
    if len(move) > 0:
        for action in move:
            new_state = copy.deepcopy(state)
            new_state.operate(action, side)
            new_state.battle(action[2])
            after_move.append([new_state, action, side])
    else:
        for action in find_legal_operations(state, side).values():
            moves = moves + action
        for action in moves:
            new_state = copy.deepcopy(state)
            new_state.operate(action, side)
            new_state.battle(action[2])
            after_move.append([new_state, action, side])

    ratio = round(len(after_move) * 0.6)

    if ismax == 1:
        after_move.sort(key=sort_evaluation)
        after_move.reverse()
        return after_move[0: ratio]
    elif ismax == 0:
        after_move.sort(key=sort_evaluation)
        return after_move[0: ratio]

    return after_move


def sort_evaluation(elem):
    return evaluation(elem[0], elem[2])


def alpha_beta_minimax(state, depth, max_player, side, alpha, beta, count=0):
    if depth == 0 or check_win(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        if depth >= 2:
            move = simulation(state, side, [], 1)
        else:
            move = simulation(state, side, [], -1)
        for new_board in move:
            utility = alpha_beta_minimax(new_board[0], depth - 1, False, side, alpha, beta, count)[0]
            count += 1
            # print(count)
            cur_max = max(cur_max, utility)
            if cur_max == utility:
                best_move = new_board[1]
            alpha = max(alpha, utility)
            if beta <= alpha:
                break
        return cur_max, best_move

    else:
        cur_min = float('inf')
        best_move = None
        if depth >= 2:
            move = simulation(state, side, [], 0)
        else:
            move = simulation(state, side, [], -1)
        for new_board in move:
            utility = alpha_beta_minimax(new_board[0], depth - 1, True, side, alpha, beta, count)[0]
            count += 1
            # print(count)
            cur_min = min(utility, cur_min)
            if cur_min == utility:
                best_move = new_board[1]
            beta = min(beta, utility)
            if beta <= alpha:
                break
        return cur_min, best_move


def check_win(state):
    flag = False
    upper_tokens = []
    lower_tokens = []
    for tokens in state[1]:
        upper_tokens.append(tokens)
    for tokens in state[0]:
        lower_tokens.append(tokens)

    up_notoks = len(upper_tokens) == 0 and state[2][1] == 0
    lo_notoks = len(lower_tokens) == 0 and state[2][0] == 0

    if up_notoks:
        flag = True
    if lo_notoks:
        flag = True

    return flag
