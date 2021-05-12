import random

"""
find all legal move for the current game with side specified
"""


def find_legal_operations(state, side):
    # throw should not be put in the first of the action since it is big

    action_list = {"SWING": [], "SLIDE": [], "THROW": []}

    # generate the throw
    Hex_range = range(-4, 4 + 1)
    type_token = ['r', 's', 'p']

    # num_left = state.throws_left[side]
    num_left = state[2][side]

    # side is 1/ 0 which denote if the palyer is upper or lower
    # problem is how to reduce the size of it ?

    if num_left > 0:
        for r in range(- 4 + (num_left - 1) * side, 5 + (side - 1) * (num_left - 1)):
            for q in Hex_range:
                if -r - q in Hex_range:
                    for token_type in type_token:
                        action_list.get("THROW").append(("THROW", token_type, (r, q)))

    # generate the slide

    token_list = []
    if side == 1:
        for tok_list in state[1].values():
            token_list += tok_list
    else:
        for tok_list in state[0].values():
            token_list += tok_list

    # print("token_list = {a}".format(a = token_list))
    for token in token_list:
        to_slide = adjacent_token(token)
        for to_go in to_slide:
            action_list.get("SLIDE").append(("SLIDE", (token[0]), (to_go)))
            for other_token in token_list:
                if other_token[0] == to_go:
                    to_swing = list(set(adjacent_token(other_token)) - set(to_slide) - {token[0]})
                    for swing in to_swing:
                        action_list.get("SWING").append(("SWING", (token[0]), (swing)))

    return action_list


"""
find ordered moves for the current game with speified side
"""


def find_advanced_operations(state, side, minimax):
    action_list = {"SWING": [], "SLIDE": [], "THROW": []}

    # generate the throw
    Hex_range = range(-4, 4 + 1)

    if side:
        type_num_our = [len(state[1].get("R")), len(state[1].get("S")), len(state[1].get("P"))]
        type_num_ad = [len(state[0].get("s")), len(state[0].get("p")), len(state[0].get("r"))]
    else:
        type_num_our = [len(state[0].get("r")), len(state[0].get("s")), len(state[0].get("p"))]
        type_num_ad = [len(state[1].get("S")), len(state[1].get("P")), len(state[1].get("R"))]

    type_diff = {"r": 0, "s": 0, "p": 0}

    i = 0

    for t, dif in type_diff.items():
        type_diff[t] = type_num_our[i] - type_num_ad[i]
        i += 1

    type_token = sorted(type_diff.keys(), reverse=minimax)

    token_list = []
    if side == 1:
        for type_tok in type_token:
            token_list += state[1][type_tok.upper()]
    else:
        for type_tok in type_token:
            token_list += state[0][type_tok]

    # num_left = state.throws_left[side]
    num_left = state[2][side]

    # side is 1/ 0 which denote if the palyer is upper or lower
    # problem is how to reduce the size of it ?

    left_bound = - 4 + (num_left - 1) * side
    right_bound = 5 + (side - 1) * (num_left - 1)

    if num_left > 0:
        for token_type in type_token:
            for r in range(left_bound, right_bound):
                for q in Hex_range:
                    if -r - q in Hex_range:
                        action_list.get("THROW").append(("THROW", token_type, (r, q)))

    # generate the slide

    # print("token_list = {a}".format(a = token_list))
    for token in token_list:
        to_slide = adjacent_token(token)
        for to_go in to_slide:
            action_list.get("SLIDE").append(("SLIDE", (token[0]), (to_go)))
            for other_token in token_list:
                if other_token[0] == to_go:
                    to_swing = list(set(adjacent_token(other_token)) - set(to_slide) - {token[0]})
                    for swing in to_swing:
                        action_list.get("SWING").append(("SWING", (token[0]), (swing)))

    return action_list


"""
random generate at least 2 moves
"""


def find_abitary_move(state, side):
    action_dict = find_legal_operations(state, side)

    abitary = []

    throws = action_dict["THROW"]
    throws_num = len(throws)
    slides = action_dict["SLIDE"]
    slides_num = len(slides)
    swings = action_dict["SWING"]
    swings_num = len(swings)

    if throws_num > 0:
        throw = random.randint(throws_num // 2, throws_num - 1)
        abitary.append(throws[throw])

    if slides_num > 0:
        slide = random.randint(0, slides_num - 1)
        abitary.append(slides[slide])

    if swings_num > 0:
        swing = random.randint(0, swings_num - 1)
        abitary.append(swings[swing])

    if len(abitary) < 2:
        if throws_num > 3 * 5:
            throw2 = random.randint(0, throws_num // 2)
            abitary.append(throws[throw2])

    return abitary


# token : [(x,y),"type"]
"""
find adjacent coordinate with given coordinate
"""


def adjacent_token(token):
    # print("token : {t}".format(t = token))

    Hex_range = range(-4, 4 + 1)

    rt, qt = token[0]

    neighbour = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    adjacent = []

    for (r, q) in neighbour:
        if -(rt + r) - (qt + q) in Hex_range and rt + r in Hex_range and qt + q in Hex_range:
            adjacent.append(((rt + r), (qt + q)))

    return adjacent


"""
evaluation function
"""


def evaluation(state, side):
    evaluation_point = 0

    defeat = {"r": "s", "p": "r", "s": "p"}
    defeated = {"r": "p", "p": "s", "s": "r"}

    # upper_tokens = state.upper_dict
    # lower_tokens = state.lower_dict

    pair_num_defeat1 = [0, 0, 0]
    pair_num_defeat2 = [0, 0, 0]

    relatively_distance1 = [0, 0, 0]
    relatively_distance2 = [0, 0, 0]

    weight1 = [-1, 1]
    weight2 = [1, -1]
    weight_token_difference = 10
    weight_throw_left = 5

    upper_tokens = state[1]
    lower_tokens = state[0]

    i = 0

    for (strong, weak) in defeat.items():

        pair_num_defeat1[i] = min(len(upper_tokens.get(strong.upper())), len(lower_tokens.get(weak)))
        if pair_num_defeat1[i] != 0:
            relatively_distance1[i] = find_relative_distance(upper_tokens.get(strong.upper()), lower_tokens.get(weak))
        i += 1

    j = 0

    for (weak, strong) in defeated.items():

        pair_num_defeat2[j] = min(len(upper_tokens.get(weak.upper())), len(lower_tokens.get(strong)))
        if pair_num_defeat2[j] != 0:
            relatively_distance2[j] = find_relative_distance(upper_tokens.get(weak.upper()), lower_tokens.get(strong))
        j += 1

    for k in range(0, 3):
        evaluation_point += (
                weight1[side] * pair_num_defeat1[k] * relatively_distance1[k] + weight2[side] * pair_num_defeat2[
            k] * relatively_distance2[k])

    # difference of the num_tokens (without throw number)
    '''
    num_diff = (state.token_left[1] + state.throws_left[1]) - (state.token_left[0] + state.throws_left[0])
    if not side:
        num_diff *= -1
    evaluation_point += num_diff*weight_token_difference
    '''
    num_diff = (state[3][1] + state[2][1]) - (state[3][0] + state[2][0])
    if not side:
        num_diff *= -1
    evaluation_point += num_diff * weight_token_difference

    # predict part

    throw_dif = state[2][0] - state[2][1]
    if side:
        throw_dif *= -1
    evaluation_point += throw_dif * weight_throw_left

    return evaluation_point


"""
calculate the distance of two tokens
"""


def find_relative_distance(upper_tokens, lower_tokens):
    # print("upper_tokens {a}  lower_tokens {b}".format(a =up_tokens, b = low_tokens ))

    total_distance = 0

    max_dis = 8

    for our in upper_tokens:
        for opponent in lower_tokens:
            temp = find_distance(our[0], opponent[0])
            total_distance += temp * (1 - (8 - temp) * 0.1)

    # negative relative
    relative_distance = total_distance / (len(upper_tokens) * len(lower_tokens))
    return 10 - relative_distance


def find_distance(start, end):
    # print("start {a}, end : {b}".format(a = start, b= end))

    dis = abs(start[0] - end[0]) + abs(start[1] - end[1]) + abs(
        start[0] - end[0] + start[1] - end[1]) - max(
        abs(start[0] - end[0]), abs(start[1] - end[1]),
        abs(start[0] - end[0] + start[1] - end[1]))

    return dis

