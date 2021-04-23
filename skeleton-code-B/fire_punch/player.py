

from fire_punch.Graph import Graph
from fire_punch.Token import Token


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
        self.graph = Graph()
        self.side = player
        self.throws = 0
        self.num_tokens = 0
        self.tokens = {}
        self.enemy_tokens = {}
        self.upper = []
        self.lower = []
        self.enemy = 'NA'
        if player == 'upper':
            self.enemy = 'lower'
        else:
            self.enemy = 'upper'

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
        self.operate(opponent_action, self.enemy)
        self.operate(player_action, self.side)
        self.battle(self.graph.hex_dict.get(opponent_action[2]))
        self.battle(self.graph.hex_dict.get(opponent_action[2]))
        # update the graph

    def battle(self, current_hex):
        if not current_hex.tokens:
            return 1
        if current_hex.get_required_tokens('r') and current_hex.get_required_tokens(
                's') and current_hex.get_required_tokens('p'):
            for rock in current_hex.get_required_tokens('r'):
                if rock in self.upper:
                    self.upper.remove(rock)
                if rock in self.lower:
                    self.lower.remove(rock)
            for scissors in current_hex.get_required_tokens('s'):
                if scissors in self.upper:
                    self.upper.remove(scissors)
                if scissors in self.lower:
                    self.lower.remove(scissors)
            for punch in current_hex.get_required_tokens('p'):
                if punch in self.upper:
                    self.upper.remove(punch)
                if punch in self.lower:
                    self.lower.remove(punch)
        if current_hex.get_required_tokens('r') and current_hex.get_required_tokens('s'):
            for scissor in current_hex.get_required_tokens('s'):
                current_hex.tokens.remove(scissor)
                if scissor in self.upper:
                    self.upper.remove(scissor)
                    # print(" upper Sci : {coor}".format(coor = scissor.coordinate))
                if scissor in self.lower:
                    self.lower.remove(scissor)
                    # print(" lower Sci : {coor}".format(coor = scissor.coordinate))
                    if current_hex.get_required_tokens('s'):
                        print("# remove failure")
        if current_hex.get_required_tokens('s') and current_hex.get_required_tokens('p'):
            for punch in current_hex.get_required_tokens('p'):
                current_hex.tokens.remove(punch)
                if punch in self.upper:
                    self.upper.remove(punch)
                    # print(" upper Punch : {coor}".format(coor = punch.coordinate))
                if punch in self.lower:
                    self.lower.remove(punch)
                    # print("lower Punch : {coor}".format(coor = punch.coordinate))
                    if current_hex.get_required_tokens('p'):
                        print("remove failure")
        if current_hex.get_required_tokens('p') and current_hex.get_required_tokens('r'):
            for rock in current_hex.get_required_tokens('r'):
                current_hex.tokens.remove(rock)
                if rock in self.upper:
                    self.upper.remove(rock)
                    # print(" upper Rock : {coor}".format(coor = rock.coordinate))
                if rock in self.lower:
                    self.lower.remove(rock)
                    # print(" lower Rock : {coor}".format(coor = rock.coordinate))
                    if current_hex.get_required_tokens('r'):
                        print("# remove failure")

    def operate(self, action, side):

        if action[0] == 'THROW':
            if side == 'lower':
                new_token = Token(action[2], action[1])
                self.lower.append(new_token)
            if side == 'upper':
                new_token = Token(action[2], action[1].upper())
                self.upper.append(new_token)
            self.graph.hex_dict.get(action[2]).add_token(new_token)



        elif action[0] == 'SLIDE':
            symbol = 'n'
            if side == 'lower':
                for token in self.graph.hex_dict.get(action[1]).tokens:
                    if token.type.islower():
                        symbol = token.type
                        token.move(action[2], 2)
                        self.graph.hex_dict.get(action[1]).tokens.remove(token)
                        break

            if side == 'upper':
                for token in self.graph.hex_dict.get(action[1]).tokens:
                    if token.type.isupper():
                        symbol = token.type
                        token.move(action[2], 1)
                        self.graph.hex_dict.get(action[1]).tokens.remove(token)
                        break

            new_token = Token(action[2], symbol)
            self.graph.hex_dict.get(action[2]).tokens.append(new_token)



        elif action[0] == 'SWING':

            symbol = 'n'
            if side == 'lower':
                for token in self.graph.hex_dict.get(action[1]).tokens:
                    if token.type.islower():
                        symbol = token.type
                        token.move(action[2], 1)
                        self.graph.hex_dict.get(action[1]).tokens.remove(token)
                        break
            if side == 'upper':
                for token in self.graph.hex_dict.get(action[1]).tokens:
                    if token.type.isUpper():
                        symbol = token.type
                        token.move(action[2], 1)
                        self.graph.hex_dict.get(action[1]).tokens.remove(token)
                        break

            new_token = Token(action[2], symbol)
            self.graph.hex_dict.get(action[2]).tokens.append(new_token)

