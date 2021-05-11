from fire_punch.utils import find_legal_operations
from fire_punch.utils import evaluation
from fire_punch.utils import compute_matrix
from fire_punch.utils import get_expected_value
from fire_punch.utils import estimate_evaluation
from fire_punch.utils import new_turn
from fire_punch.utils import find_abitary_move
from trail.player import check_win
from trail.player import alpha_beta_minimax
from trail.player import simultaneous_move
import numpy as np
import copy
def double_oracle(state, alpha, beta, side, depth):
    utility = 0

    oppnent = 0
    if not side:
        oppnent = 1

    if check_win(state) or depth == 0:
        utility = evaluation(state, side)
        print("cutoff test")
        return utility, state

    max_val = alpha
    min_val = beta
    left_bound, move = alpha_beta_minimax(state, 2, True, side, max_val, min_val)
    right_bound = alpha_beta_minimax(state, 2, False, side, max_val, min_val)[0]
    if left_bound == right_bound or abs(left_bound - right_bound) < 1.1:
        utility = left_bound
        # print("left {a} = right {b} ".format(a = left_bound, b = right_bound))
        return utility, move
    # find arbitrary move
    my_move = []
    ad_move = []
    my_move += find_abitary_move(state, side)
    ad_move += find_abitary_move(state, oppnent)

    # key : actions i, value : [ui,j]
    pIJ = alpha_beta_minimax_limit(state, 2, True, side, max_val, min_val, copy.deepcopy(my_move),
                                   copy.deepcopy(ad_move))[0]
    oIJ = alpha_beta_minimax_limit(state, 2, False, side, max_val, min_val, copy.deepcopy(my_move),
                                   copy.deepcopy(ad_move))[0]

    # initialize the boundary of the first abitary actions

    p = [[pIJ for i in range(0, 21)] for j in range(0, 21)]
    o = [[oIJ for i in range(0, 21)] for j in range(0, 21)]

    print("pIJ = {a}, oIJ = {b}, oij = {c}, pij ={d} ".format(a=pIJ, b=oIJ, c=o[0][0], d=p[0][0]))

    while alpha != beta or abs(alpha - beta) > 0.5:
        print("enter_while")

        index_i = 0

        for i in my_move:

            index_j = 0
            for j in ad_move:

                if p[index_i][index_j] < o[index_i][index_j]:
                    new_state = simultaneous_move(state, i, j, side)

                    u_temp = double_oracle(new_state, alpha, beta, side, depth - 1)[0]

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
def alpha_beta_minimax_limit(state, depth, max_player, side, alpha, beta, max_move, min_move):
    if depth == 0 or check_win(state):
        return evaluation(state, side), state

    if max_player:
        cur_max = float('-inf')
        best_move = None
        if len(max_move) > 0:
            #print(max_move)
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
            action = simulation(state, 1 - side, min_move)
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


def BR_max(state, alpha, y, side):
    print("{a}  {b} ".format(a="br max", b=len(y)))
    br = alpha
    move = None

    action_to_maxmal = []

    for actions in find_legal_operations(state, side).values():
        action_to_maxmal += actions

    p = []
    o = []

    for i in range(0, len(action_to_maxmal)):

        piJ = alpha_beta_minimax_limit(state, 2, True, side, float('-inf'), float('inf'), [action_to_maxmal[i]],
                                       list(y.keys()))[0]

        oiJ = alpha_beta_minimax_limit(state, 2, False, side, float('-inf'), float('inf'), [action_to_maxmal[i]],
                                       list(y.keys()))[0]

        # initialise the boudary
        p = [piJ for i in range(0, len(y))]
        o = [oiJ for i in range(0, len(y))]

        utility = [-1000 for i in range(0, len(y))]
        utility = np.array(utility)

        j = 0

        if list(y.values())[j] > 0 and p[j] < o[j]:

            for action, prob in y.items():

                pij_estimate = max(p[j], br - estimate_evaluation(y, o[j], action))

                if pij_estimate > o[j]:
                    continue
                else:
                    new_state = new_turn(side, state, action_to_maxmal[i], action)
                    utility[j] = double_oracle(new_state, p[j], o[j], side, 3)[0]
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

        piJ = alpha_beta_minimax_limit(state, 2, True, side, float('-inf'), float('inf'), [action_to_minimal[i]],
                                       list(x.keys()))[0]
        oiJ = alpha_beta_minimax_limit(state, 2, False, side, float('-inf'), float('inf'), [action_to_minimal[i]],
                                       list(x.keys()))[0]

        # initialise the boudary
        p = [piJ for i in range(0, len(x))]
        o = [oiJ for i in range(0, len(x))]

        utility = [1000 for i in range(0, len(x))]
        utility = np.array(utility)
        j = 0

        if list(x.values())[j] > 0 and p[j] < o[j]:

            for action, prob in x.items():

                pij_estimate = min(o[j], br - estimate_evaluation(x, p[j], action))

                if pij_estimate < p[j]:
                    continue
                else:
                    new_state = new_turn(side, state, action_to_minimal[i], action)
                    utility[j] = double_oracle(new_state, p[j], o[j], side, 3)[0]
                    p[j] = utility[j]
                    o[j] = utility[j]

        # if have been calculate

        expected = get_expected_value(x, utility)
        if expected < br:
            move = action_to_minimal[i]
            br = expected

    return move, br

