from fire_punch.State import State
from fire_punch.Token import Token
from fire_punch.utils import find_legal_operations
from fire_punch.utils import evaluation
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

        return alpha_beta_minimax(self.state, 2, True, self.side, float('-inf'), float('inf'))[1]

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


def re_minimax(state, depth, max_player, side):
    if depth == 0:
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        for new_board in simulation(state, side):
            utility = re_minimax(new_board[0], depth - 1, False, side)[0]
            cur_max = max(cur_max, utility)
            if cur_max == utility:
                best_move = new_board[1]

        return cur_max, best_move
    else:
        cur_min = float('inf')
        best_move = None
        for new_board in simulation(state, 1 - side):
            utility = re_minimax(new_board[0], depth - 1, True, side)[0]
            cur_min = min(cur_min, utility)
            if cur_min == utility:
                best_move = new_board[1]

        return cur_min, best_move


def alpha_beta_minimax(state, depth, max_player, side, alpha, beta):
    if depth == 0 or check_win_draw(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        for new_board in simulation(state, side):
            utility = alpha_beta_minimax(new_board[0], depth - 1, False, side, alpha, beta)[0]
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
        for new_board in simulation(state, 1 - side):
            utility = alpha_beta_minimax(new_board[0], depth - 1, True, side, alpha, beta)[0]
            cur_min = min(utility, cur_min)
            if cur_min == utility:
                best_move = new_board[1]
            beta = min(beta, utility)
            if beta <= alpha:
                break
        return cur_min, best_move


def simulation(state, side):
    moves = []
    after_move = []
    for action in find_legal_operations(state, side).values():
        moves = moves + action
    for action in moves:
        new_state = copy.deepcopy(state)
        new_state.operate(action, side)
        new_state.battle(action[2])
        after_move.append([new_state, action])
    return after_move


def check_win_draw(state):
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




player = Player("upper")
player.state.operate(("THROW", "s", (4, -4)), 1)
player.state.operate(("THROW", "p", (-4, 0)), 0)

print(re_minimax(player.state, 2, True, 1))
print(alpha_beta_minimax(player.state, 2, True, 1, float('-inf'), float('inf')))
print("------end------")

# only throw action

# distinguish side
