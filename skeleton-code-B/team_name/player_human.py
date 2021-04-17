
from Graph import Graph 

class Player:

    #global constant 
    
    maximum_tokens = 9


    #global variable
    
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
        self.side  = player
        self.throws = 0
        self.num_tokens = 0
        self.tokens = {}
        self.enemy_tokens = {}

        
        

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        action_list = []


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
        
        #update the graph

        
    
    
    
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