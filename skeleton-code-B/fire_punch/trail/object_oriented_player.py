import sys

sys.path.append('../..')

from trail.State import State
from team_strategy import find_legal_operations
from team_strategy import evaluation

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
        self.state = State()
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

        move = alpha_beta_minimax(self.state, 3, True, self.side, float('-inf'), float('inf'))[1]

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
        self.state.operate(opponent_action, self.enemy)
        self.state.operate(player_action, self.side)
        self.state.battle(opponent_action[2])
        self.state.battle(player_action[2])
        # update the graph


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


def simultaneous_move(state, move1, move2, side):
    new_state = copy.deepcopy(state)
    new_state.operate(move1, side)
    new_state.operate(move2, 1 - side)
    new_state.battle(move1[2])
    new_state.battle(move2[2])

    return new_state


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
    # return after_move


def sort_evaluation(elem):
    return evaluation(elem[0], elem[2])


def check_win(state):
    flag = False
    upper_tokens = []
    lower_tokens = []
    for tokens in state.upper_dict.values():
        upper_tokens.append(tokens)
    for tokens in state.lower_dict.values():
        lower_tokens.append(tokens)

    up_notoks = len(upper_tokens) == 0 and state.throws_left[1] == 0
    lo_notoks = len(lower_tokens) == 0 and state.throws_left[0] == 0

    if up_notoks:
        flag = True
    if lo_notoks:
        flag = True

    return flag



list = [7,1,3,4]
list = sorted(list, reverse=False)
print(list)



# print(alpha_beta_minimax(player.state, 4, False, 1, float('-inf'), float('inf')))
print("------end------")
