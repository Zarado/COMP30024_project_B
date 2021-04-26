from State import State
from Token import Token




def find_legal_operations(state, side):
    
    action_list = {"THROW":[], "SLIDE":[], "SWING":[]}

    #generate the throw 
    Hex_range = range(-4,4 + 1)
    type_token = ['r','s','p']

    num_left = state.throws_left[side]

    #side is 1/ 0 which denote if the palyer is upper or lower 
    #problem is how to reduce the size of it ?

    if num_left > 0:
        for r in range( - 4  + (num_left - 1)*side , 5 + (side - 1 )*(num_left - 1) ):
            for q in Hex_range:
                if -r - q in Hex_range:
                    for token_type in type_token:
                        action_list.get("THROW").append(("THROW",token_type,(r,q)))

    
    #generate the slide 

   

    token_list = []
    if side == 1:
        for tok_list in state.upper_dict.values():
            token_list + tok_list
    else:
        for tok_list in state.lower_dict.values():
            token_list + tok_list


    for token in token_list:
        to_slide  = adjacent_token(token)
        for to_go in to_slide:
            action_list.get("SLIDE").append(("SLIDE",(token.coordinate),(to_go)))
            for other_token in token_list:
                if other_token.coordinate == to_go:
                    to_swing = list( set(adjacent_token(other_token)) - set(to_slide) - {token.coordinate} )
                    for swing in to_swing:
                        action_list.get("SWING").append(("SWING",(token.coordinate),(swing)))
    
    return action_list



def adjacent_token(token):

    Hex_range = range(-4,4 + 1)

    rt,qt = token.coordinate

    neighbour = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    adjacent = []

    for (r,q) in neighbour:
        if -(rt + r) - (qt + q) in Hex_range and rt + r in Hex_range and qt + q in Hex_range:
            adjacent.append(((rt + r), (qt + q)))
    
    return adjacent



def evaluation(state,side):

    evaluation_point = 0
    
    defeat = {"r": "s", "p": "r", "s": "p"}
    defeated = {"r": "p", "p": "s", "s": "r"}

    upper_tokens = state.upper_dict
    lower_tokens = state.lower_dict

    pair_num_defeat1 = [0,0,0]
    pair_num_defeat2 = [0,0,0]
    
    relatively_distance1 = [0,0,0]
    relatively_distance2 = [0,0,0]
    
    weight1 = [-1,1]
    weight2 = [1,-1]

    
    i = 0
    
    for (strong,weak) in defeat.items():

        pair_num_defeat1[i] = min(len(upper_tokens.get(strong.upper())), len(lower_tokens.get(weak)) )
        if pair_num_defeat1[i] !=  0:
            relatively_distance1[i] = find_relative_distance(upper_tokens.get(strong.upper()), lower_tokens.get(weak))
        i += 1
    
    j = 0


    for (weak,strong) in defeated.items():


        pair_num_defeat2[j] = min(len(upper_tokens.get(weak.upper())), len(lower_tokens.get(strong)) )
        if pair_num_defeat2[j] != 0:
            relatively_distance2[j] = find_relative_distance(upper_tokens.get(weak.upper()), lower_tokens.get(strong))
        j += 1
    
    
    
    for k in range(0,3):
        
        evaluation_point += (weight1[side]*pair_num_defeat1[k]*relatively_distance1[k] + weight2[side]*pair_num_defeat2[k]*relatively_distance2[k])
    
    #predict part 

    throw_dif = state.throws_left[0] - state.throws_left[1]
    if side:
        throw_dif *= -1
    evaluation_point += throw_dif

    return evaluation_point


def find_relative_distance(upper_tokens, lower_tokens):

    total_distance = 0


    for our in upper_tokens:
        for opponent in lower_tokens:
            total_distance += find_distance(our,opponent)

    #negative relative 
    return 10 - (total_distance/(len(upper_tokens)*len(lower_tokens)))


def find_distance(start, end):


    dis = abs(start.coordinate[0] - end.coordinate[0]) + abs(start.coordinate[1] - end.coordinate[1]) + abs(
        start.coordinate[0] - end.coordinate[0] + start.coordinate[1] - end.coordinate[1]) - max(
        abs(start.coordinate[0] - end.coordinate[0]), abs(start.coordinate[1] - end.coordinate[1]),
        abs(start.coordinate[0] - end.coordinate[0] + start.coordinate[1] - end.coordinate[1]))
    return dis

'''

ts = State()
ts.upper_dict.get("R").append(Token((4,-4),"R"))
ts.upper_dict.get("S").append(Token((3,-3),"S"))

ts.lower_dict.get("s").append(Token((-4,0),"s"))
ts.lower_dict.get("s").append(Token((-4,4),"s"))
ts.lower_dict.get("p").append(Token((-2,-2),"p"))

ts.throws_left[0] = 6
ts.throws_left[1] = 7

print(evaluation(ts,1))


'''