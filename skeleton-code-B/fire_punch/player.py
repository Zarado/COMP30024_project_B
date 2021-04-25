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

        return action_list

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
        self.battle(opponent_action[2])
        self.battle(player_action[2])
        # update the graph

    def battle(self, coordinate):
        battle_list = []
        for dict_val in self.state.upper_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type.lower() not in battle_list:
                        battle_list.append(token.type.lower())

        for dict_val in self.state.lower_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type not in battle_list:
                        battle_list.append(token.type.lower())

        if len(battle_list) == 3:
            self.state.remove_coordinate(coordinate, "all")

        if len(battle_list) == 2:

            if "r" in battle_list and "s" in battle_list:
                self.state.remove_coordinate(coordinate, "s")

            if "r" in battle_list and "p" in battle_list:
                self.state.remove_coordinate(coordinate, "r")

            if "p" in battle_list and "s" in battle_list:
                self.state.remove_coordinate(coordinate, "p")


'''
    def operate(self, action, side):

        if action[0] == "THROW":
            if side == "lower":
                new_token = Token(action[2], action[1])
                self.state.lower_dict.get(new_token.type).append(new_token)
                self.state.throws_left[0] -= 1
            if side == "upper":
                new_token = Token(action[2], action[1].upper())
                self.state.upper_dict.get(new_token.type).append(new_token)
                self.state.throws_left[1] -= 1

        elif action[0] == "SLIDE" or "SWING":

            if side == "lower":
                for token in self.state.lower_dict["s"] + self.state.lower_dict["r"] + self.state.lower_dict["p"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)

            if side == "upper":
                for token in self.state.upper_dict["S"] + self.state.upper_dict["R"] + self.state.upper_dict["P"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)
             '''


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


def minimax(state):
    upper_action = {}
    lower_action = {}
    upper_moves = []
    lower_moves = []
    pivot = 0

    for moves in find_legal_operations(state, 1).values():
        upper_moves = upper_moves + moves

    for moves in find_legal_operations(state, 0).values():
        lower_moves = lower_moves + moves

    for actions in upper_moves:
        simulation = copy.deepcopy(state)
        simulation.operate(actions, 1)
        for lower_actions in lower_moves:
            simulation1 = copy.deepcopy(simulation)
            simulation1.operate(lower_actions, 0)
            lower_action[pivot] = evaluation(simulation1, 1)
            pivot += 1
        upper_action[upper_moves.index(actions)] = min(lower_action.items(), key=lambda x: x[1])
        lower_action = {}
        pivot = 0
    result = max(upper_action.items(), key=lambda x: x[1])
    return result[1][1], upper_moves[result[0]]


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


player = Player("upper")
player.state.operate(("THROW", "s", (4, -4)), 1)
player.state.operate(("THROW", "p", (-4, 0)), 0)
print(minimax(player.state))
print(re_minimax(player.state, 2, True, 1))

print("------end------")

# only throw action

# distinguish side
