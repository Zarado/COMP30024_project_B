import sys

sys.path.append('..')
from fire_punch.utils1 import find_legal_operations
from fire_punch.utils1 import evaluation
from fire_punch.utils1 import find_advanced_operations

import copy
import time


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
        if player == 'upper':
            self.side = 1
            self.enemy = 0
        else:
            self.side = 0
            self.enemy = 1
        self.turn = 0

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        if self.state[2][self.side] > 0:

            move = alpha_beta_minimax(self.state, 2, True, self.side, -1000, 1000, self.turn)[1]
        else:

            move = alpha_beta_minimax(self.state, 2, True, self.side, -1000, 1000, self.turn)[1]

        return move

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        operate(self.state, opponent_action, self.enemy)
        operate(self.state, player_action, self.side)
        battle(self.state, opponent_action[2])
        battle(self.state, player_action[2])
        self.turn += 1
        # update the graph


def simulation(state, side, move, ismax, minimax):
    moves = []
    after_move = []
    if len(move) > 0:
        for action in move:
            new_state = copy.deepcopy(state)
            operate(new_state, action, side)
            battle(new_state, action[2])
            after_move.append([new_state, action, side])
    else:
        if minimax == 1:
            for action in find_advanced_operations(state, side, False).values():
                moves = moves + action
        elif minimax == 0:
            for action in find_advanced_operations(state, side, True).values():
                moves = moves + action

        for action in moves:
            new_state = copy.deepcopy(state)
            operate(new_state, action, side)
            if minimax == 0:
                for lists in new_state[0].values():
                    for tok in lists:
                        battle(new_state, tok[0])
                for lists in new_state[1].values():
                    for tok in lists:
                        battle(new_state, tok[0])
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



def alpha_beta_minimax(state, depth, max_player, side, alpha, beta, turn):
    if depth == 0 or check_win(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        if depth >= 2:
            move = simulation(state, side, [], 1, 1)
        else:
            move = simulation(state, side, [], -1, 1)
        for new_board in move:
            utility = alpha_beta_minimax(new_board[0], depth - 1, False, side, alpha, beta, turn)[0]
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
            move = simulation(state, 1 - side, [], 0, 0)
        else:
            move = simulation(state, 1 - side, [], -1, 0)
        for new_board in move:
            utility = alpha_beta_minimax(new_board[0], depth - 1, True, side, alpha, beta, turn)[0]
            cur_min = min(utility, cur_min)
            if cur_min == utility:
                best_move = new_board[1]
            beta = min(beta, utility)

            if beta <= alpha:
                break
        return cur_min, best_move


def operate(state, action, side):
    if action[0] == "THROW":
        if side == 0:
            new_token = [action[2], action[1].lower()]
            state[0].get(new_token[1]).append(new_token)
            state[2][0] -= 1
            state[3][0] += 1
        if side == 1:
            new_token = [action[2], action[1].upper()]
            state[1].get(new_token[1]).append(new_token)
            state[2][1] -= 1
            state[3][1] += 1

    elif action[0] == "SLIDE" or "SWING":

        if side == 0:
            for act in state[0].values():
                for token in act:
                    if token[0] == action[1]:
                        token[0] = action[2]
                        break

        if side == 1:
            for act in state[1].values():
                for token in act:
                    if token[0] == action[1]:
                        token[0] = action[2]
                        break


def battle(state, coordinate):
    battle_list = []

    for action in state[0].values():
        for token in action:
            if token[0] == coordinate:
                if token[1].lower() not in battle_list:
                    battle_list.append(token[1].lower())

    for action in state[1].values():
        for token in action:
            if token[0] == coordinate:
                if token[1].lower() not in battle_list:
                    battle_list.append(token[1].lower())

    if len(battle_list) == 3:
        remove_coordinate(state, coordinate, "all")

    if len(battle_list) == 2:

        if "r" in battle_list and "s" in battle_list:
            remove_coordinate(state, coordinate, "s")

        if "r" in battle_list and "p" in battle_list:
            remove_coordinate(state, coordinate, "r")

        if "p" in battle_list and "s" in battle_list:
            remove_coordinate(state, coordinate, "p")


def remove_coordinate(state, coordinate, spices):
    if spices == "all":

        for spc in state[0].keys():
            prev = len(state[0].get(spc))
            action = [token for token in state[0].get(spc) if token[0] != coordinate]
            state[3][0] = state[3][0] - (prev - len(action))
            state[0][spc] = action

        for spc in state[1].keys():
            prev = len(state[1].get(spc))
            action = [token for token in state[1].get(spc) if token[0] != coordinate]
            state[3][1] = state[3][1] - (prev - len(action))
            state[1][spc] = action
    else:

        for spc in state[0].keys():
            prev_len = len(state[0].get(spc))
            action = [token for token in state[0].get(spc) if token[0] != coordinate or token[1] != spices.lower()]
            state[3][0] = state[3][0] - (prev_len - len(action))
            state[0][spc] = action

        for spc in state[1].keys():
            prev_len = len(state[1].get(spc))
            action = [token for token in state[1].get(spc) if token[0] != coordinate or token[1] != spices.upper()]
            state[3][1] = state[3][1] - (prev_len - len(action))
            state[1][spc] = action


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


player = Player("upper")
operate(player.state, ("THROW", "s", (4, -4)), 1)
operate(player.state, ("THROW", "s", (4, -4)), 1)
operate(player.state, ("THROW", "r", (-4, 0)), 0)
start = time.time()
print(time.time() - start)
