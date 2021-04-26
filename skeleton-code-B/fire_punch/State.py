class State:
    def __init__(self):
        self.upper_dict = {"R": [], "P": [], "S": []}
        self.lower_dict = {"r": [], "p": [], "s": []}
        self.throw_left = 9

        #0 denote lower, 1 denote upper
        self.throws_left = [9,9]

    def remove_coordinate(self, coordinate, spices):
        if spices == "all":
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token.coordinate == coordinate:
                        self.upper_dict.get(key).remove(token)
            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token.coordinate == coordinate:
                        self.lower_dict.get(key).remove(token)
        else:
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token.coordinate == coordinate and token.type.lower() == spices:
                        self.upper_dict.get(key).remove(token)
            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token.coordinate == coordinate and token.type.lower() == spices:
                        self.lower_dict.get(key).remove(token)
