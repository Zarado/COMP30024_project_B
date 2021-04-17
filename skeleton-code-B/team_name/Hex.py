"""
class hex contain the information of each hex on the board (node of a graph) include
its coordinate, the neighbour of this token and the token currently
on the hex.
"""


class Hex:

    def __init__(self, coordinate):
        self.neighbour = []
        self.tokens = []
        self.coordinate = coordinate

    def add_neighbour(self, new_hex):
        self.neighbour.append(new_hex)

    def add_token(self, token):
        self.tokens.append(token)

    # find the token with required type and add them to a list to return
    def get_required_tokens(self, required_type):
        temp = []
        for token in self.tokens:
            if required_type == token.type:
                temp.append(token)
        return temp
    def print_neighbour(self):
        for i in self.neighbour:
            print(i.coordinate)


