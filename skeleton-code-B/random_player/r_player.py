from random_player.State import State
from fire_punch.utils import find_legal_operations
from fire_punch.utils import find_abitary_move
from fire_punch.utils import evaluation

import copy
import random


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
        after = find_abitary_move(self.state, self.side)

        move = random.randint(0, len(after) - 1)

        if self.side == 1:
            while after[move][2] in self.state.upper_dict.values():
                move = random.randint(0, len(after))

        if self.side == 0:
            while after[move][2] in self.state.lower_dict.values():
                move = random.randint(0, len(after))
        # for list in self.state.lower_dict.values():
        #   for tok in list:
        #      print(tok.type, tok.coordinate)`

        afters = simulation(self.state, self.side)
        afters.sort(key=eval_sort)

        return after[move]

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


def simulation(state, side):
    moves = []
    after_move = []
    for action in find_legal_operations(state, side).values():
        moves = moves + action
    for action in moves:
        new_state = copy.deepcopy(state)
        new_state.operate(action, side)
        new_state.battle(action[2])
        after_move.append([new_state, action, side])
    return after_move


def eval_sort(elem):
    return evaluation(elem[0], elem[2])

# throw
