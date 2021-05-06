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

        # move = alpha_beta_minimax(self.state, 2, True, self.side, float('-inf'), float('inf'))[1]
        move = double_oracle(self.state, float('-inf'), float('inf'), player.side)[1]

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


def alpha_beta_minimax_limit(state, depth, max_player, side, alpha, beta, max_move, min_move):
    if depth == 0 or check_win(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        if len(max_move) > 0:
            action = simulation(state, side, max_move)
            max_move.clear()
        else:
            action = simulation(state, side, [])
        for new_board in action:
            utility = alpha_beta_minimax_limit(new_board[0], depth - 1, False, side, alpha, beta, max_move, min_move)[0]
            cur_max = max(cur_max, utility)
            if cur_max == utility:
                best_move = new_board[1]
            alpha = max(alpha, utility)
            if beta <= alpha:
                break
        return cur_max, best_move,

    else:
        cur_min = float('inf')
        best_move = None
        if len(min_move) > 0:
            action = simulation(state, side, min_move)
            min_move.clear()
        else:
            action = simulation(state, 1 - side, [])
        for new_board in action:
            utility = alpha_beta_minimax_limit(new_board[0], depth - 1, True, side, alpha, beta, max_move, min_move)[0]
            cur_min = min(utility, cur_min)
            if cur_min == utility:
                best_move = new_board[1]
            beta = min(beta, utility)
            if beta <= alpha:
                break
        return cur_min, best_move


def alpha_beta_minimax(state, depth, max_player, side, alpha, beta, count=0):
    if depth == 0 or check_win(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        for new_board in simulation(state, side, []):
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
        for new_board in simulation(state, 1 - side, []):
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


# -------------------------------------------double oracle---------------------------------------------
def double_oracle(state, alpha, beta, side):
    utility = 0

    oppnent = 0
    if not side:
        oppnent = 1

    if check_win(state):
        utility = evaluation(state, side)
        print("cutoff test")
        return utility, state

    max_val = float('-inf')
    min_val = float('inf')
    left_bound, move = alpha_beta_minimax(state, 2, True, side, max_val, min_val)
    right_bound = alpha_beta_minimax(state, 2, False, side, max_val, min_val)[0]
    if left_bound == right_bound:
        utility = left_bound
        print("alpha = beta")
        return utility, move
    # find arbitrary move
    my_move = [] 
    ad_move = [] 
    my_move += find_abitary_move(state,side)
    ad_move += find_abitary_move(state,oppnent)
    new_state = simultaneous_move(state, my_move[0], ad_move[0], side)

    # key : actions i, value : [ui,j]
    pIJ = alpha_beta_minimax_limit(new_state, 2, False, side, max_val, min_val, copy.deepcopy(my_move),
                                   copy.deepcopy(ad_move))[0]
    oIJ = alpha_beta_minimax_limit(new_state, 2, True, side, max_val, min_val, copy.deepcopy(my_move),
                                   copy.deepcopy(ad_move))[0]

    # initialize the boundary of the first abitary actions

    p = [[pIJ for i in range(0, 21)] for j in range(0, 21)]
    o = [[oIJ for i in range(0, 21)] for j in range(0, 21)]

    print("pIJ = {a}, oIJ = {b}, oij = {c}, pij ={d} ".format(a=pIJ, b=oIJ, c=o[0][0], d=p[0][0]))

    while alpha != beta:
        print("enter_while")

        index_i = 0

        for i in my_move:

            index_j = 0
            for j in ad_move:

                if p[index_i][index_j] < o[index_i][index_j]:
                    new_state = simultaneous_move(state, i, j, side)

                    u_temp = double_oracle(new_state, alpha, beta, side)[0]

                    p[index_i][index_j] = u_temp
                    o[index_i][index_j] = u_temp

                index_j += 1
        index_i += 1

        # end for loop

        my_strategy = []
        ad_strategy = []

        temp_output_NE = compute_matrix(state, 1, side, my_move, ad_move)
        utility = temp_output_NE[0]
        my_strategy = temp_output_NE[1]
        ad_strategy = temp_output_NE[2]

        bsmax = BR_max(state, alpha, ad_strategy, side)
        bsmin = BR_min(state, beta, my_strategy, oppnent)
        

        if bsmax[0] == None:
            print("bsmax none")
            return min_val, my_move[-1]
        elif bsmin[0] == None:
            print("bsmin none")
            return max_val, my_move[-1]

        alpha = max(alpha, bsmin[1])

        beta = min(beta, bsmax[1])

        print(alpha)
        print(beta)

        # add the new action to the actions list
        my_move.append(bsmax[0])
        ad_move.append(bsmin[0])

        print("run out of the double oracle")
        print(my_move[-1])

    return utility, my_move[-1]


def BR_max(state, alpha, y, side):
    br = alpha
    move = None

    action_to_maxmal = []



    for actions in find_legal_operations(state, side).values():
        action_to_maxmal += actions
    

    p = []
    o = []

    for i in range(0, len(action_to_maxmal)):

        piJ = alpha_beta_minimax_limit(state, 2, False, side, float('-inf'), float('inf'), [action_to_maxmal[i]],
                                       list(y.keys()))[0]
        oiJ = alpha_beta_minimax_limit(state, 2, True, side, float('-inf'), float('inf'), [action_to_maxmal[i]],
                                       list(y.keys()))[0]

        # initialise the boudary
        p = [piJ for i in range(0, len(y))]
        o = [oiJ for i in range(0, len(y))]

        utility = [-1000 for i in range(0,len(y))]
        utility = np.array(utility)

        j = 0

        if list(y.values())[j] > 0 and p[j] < o[j]:

            for action, prob in y.items():

                pij_estimate = max(p[j], br - estimate_evaluation(y, o[j], action))

                if pij_estimate > o[j]:
                    continue
                else:
                    new_state = new_turn(side, state, action_to_maxmal[i], action)
                    utility[j] = double_oracle(new_state, p[j], o[j])[0]
                    p[j] = utility[j]
                    o[j] = utility[j]

        # if have been calculate

        expected = get_expected_value(y, utility)
        
        if expected > br:
            
            move = action_to_maxmal[i]
            br = expected

    return move, br


def BR_min(state, beta, x, side):
    br = beta
    move = None

    action_to_minimal = []

    for actions in find_legal_operations(state, side).values():
        action_to_minimal += actions

    p = []
    o = []

    for i in range(0, len(action_to_minimal)):

        piJ = alpha_beta_minimax_limit(state, 2, False, side, float('-inf'), float('inf'), [action_to_minimal[i]],
                                       list(x.keys()))[0]
        oiJ = alpha_beta_minimax_limit(state, 2, True, side, float('-inf'), float('inf'), [action_to_minimal[i]],
                                       list(x.keys()))[0]

        # initialise the boudary
        p = [piJ for i in range(0, len(x))]
        o = [oiJ for i in range(0, len(x))]

        utility = [1000 for i in range(0,len(x))]
        utility = np.array(utility)
        j = 0

        if list(x.values())[j] > 0 and p[j] < o[j]:

            for action, prob in x.items():

                pij_estimate = min(o[j], br - estimate_evaluation(x, p[j], action))

                if pij_estimate < p[j]:
                    continue
                else:
                    new_state = new_turn(side, state, action_to_minimal[i], action)
                    utility[j] = double_oracle(new_state, p[j], o[j])[0]
                    p[j] = utility[j]
                    o[j] = utility[j]

        # if have been calculate

        expected = get_expected_value(x, utility)
        if expected < br:
            move = action_to_minimal[i]
            br = expected


    return move, br


def simultaneous_move(state, move1, move2, side):
    new_state = copy.deepcopy(state)
    new_state.operate(move1, side)
    new_state.operate(move2, 1 - side)
    new_state.battle(move1[2])
    new_state.battle(move2[2])

    return new_state


# -------------------------------------------helper---------------------------------------------


def simulation(state, side, move):
    moves = []
    after_move = []
    if (len(move) > 0):
        for action in move:
            new_state = copy.deepcopy(state)
            new_state.operate(action, side)
            new_state.battle(action[2])
            after_move.append([new_state, action])
    else:
        for action in find_legal_operations(state, side).values():
            moves = moves + action
        for action in moves:
            new_state = copy.deepcopy(state)
            new_state.operate(action, side)
            new_state.battle(action[2])
            after_move.append([new_state, action])
    return after_move


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


player = Player("upper")
player.state.operate(("THROW", "s", (4, -4)), 1)
player.state.operate(("THROW", "p", (-4, 0)), 0)
counter = [1]

print(double_oracle(player.state, -100, 100, 1))

# print(alpha_beta_minimax(player.state, 4, True, 1, float('-inf'), float('inf')))
# print(alpha_beta_minimax(player.state, 4, False, 1, float('-inf'), float('inf')))
print("------end------")
