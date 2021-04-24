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
    
    defeat = {"r": "s", "p": "r", "s": "p"}
    defeated = {"r": "p", "p": "s", "s": "r"}

    our_tokens = {}
    opponent_tokens = {}

    pair_num_defeat = [0,0,0]
    
    relatively_distance1 = [0,0,0]
    relatively_distance2 = [0,0,0]
    
    weight1 = 1
    weight2 = -1

    if side == 1 :
        our_tokens = state.upper_dict
        opponent_tokens = state.lower_dict
    else:
        our_tokens = state.lower_dict
        opponent_tokens = state.upper_dict

    i = 0
    for (strong,weak) in defeat.items():
        pair_num_defeat[i] = min(len(our_tokens.get(strong.upper())), len(opponent_tokens.get(weak)) )
        relatively_distance1 = find_relative_distance(our_tokens.get(strong.upper()), opponent_tokens.get(weak))
        i += 1
    



def find_relative_distance(our_tokens, opponent_tokens):

    return 1


