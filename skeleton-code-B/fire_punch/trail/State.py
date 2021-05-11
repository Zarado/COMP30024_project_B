from trail.Token import Token


class State:
    def __init__(self):
        self.upper_dict = {"R": [], "P": [], "S": []}
        self.lower_dict = {"r": [], "p": [], "s": []}
        self.throws_left = [9, 9]
        self.token_left = [0, 0]

    def remove_coordinate(self, coordinate, spices):
        if spices == "all":
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token.coordinate == coordinate:
                        self.upper_dict.get(key).remove(token)
                        self.token_left[1] -= 1

            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token.coordinate == coordinate:
                        self.lower_dict.get(key).remove(token)
                        self.token_left[0] -= 1
        else:
            for key in self.upper_dict.keys():
                for token in self.upper_dict.get(key):
                    if token.coordinate == coordinate and token.type == spices.upper():
                        self.upper_dict.get(key).remove(token)
                        self.token_left[1] -= 1

            for key in self.lower_dict.keys():
                for token in self.lower_dict.get(key):
                    if token.coordinate == coordinate and token.type == spices.lower():
                        self.lower_dict.get(key).remove(token)
                        self.token_left[0] -= 1

    def operate(self, action, side):

        if action[0] == "THROW":
            if side == 0:
                new_token = Token(action[2], action[1].lower())
                self.lower_dict.get(new_token.type).append(new_token)
                self.throws_left[0] -= 1
                self.token_left[0] += 1
            if side == 1:
                new_token = Token(action[2], action[1].upper())
                self.upper_dict.get(new_token.type).append(new_token)
                self.throws_left[1] -= 1
                self.token_left[1] += 1

        elif action[0] == "SLIDE" or "SWING":

            if side == 0:
                for token in self.lower_dict["s"] + self.lower_dict["r"] + self.lower_dict["p"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)
                        break

            if side == 1:
                for token in self.upper_dict["S"] + self.upper_dict["R"] + self.upper_dict["P"]:
                    if token.coordinate == action[1]:
                        token.move(action[2], 2)
                        break

    def battle(self, coordinate):
        battle_list = []
        for dict_val in self.upper_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type.lower() not in battle_list:
                        battle_list.append(token.type.lower())

        for dict_val in self.lower_dict.values():
            for token in dict_val:
                if token.coordinate == coordinate:
                    if token.type.lower() not in battle_list:
                        battle_list.append(token.type.lower())

        if len(battle_list) == 3:
            self.remove_coordinate(coordinate, "all")

        if len(battle_list) == 2:

            if "r" in battle_list and "s" in battle_list:
                self.remove_coordinate(coordinate, "s")

            if "r" in battle_list and "p" in battle_list:
                self.remove_coordinate(coordinate, "r")

            if "p" in battle_list and "s" in battle_list:
                self.remove_coordinate(coordinate, "p")
