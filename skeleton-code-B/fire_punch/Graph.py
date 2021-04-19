from fire_punch.Hex import Hex


# Class graph is a hexagon that contains 61 hexagon units and the positional relationship between each unit.
class Graph:
    hex_dict = {}
    """
    initialize the graph according the size and coordinate using a dict structure of the given board
    and add all the current tokens to them.
    """
    def __init__(self):
        Hex_Range = range(-4,5)
        for r in Hex_Range:
            for q in Hex_Range:
                if -r -q in Hex_Range:
                    self.hex_dict[(r,q)] = Hex((r,q))

        for cur_hex in self.hex_dict.values():
            self.add_neighbours(cur_hex)

    # for each hex in the graph add neighbours to it.
    def add_neighbours(self, current_hex):
        neibour = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

        for (r,q) in neibour:
            if self.hex_dict.get((current_hex.coordinate[0] + r , current_hex.coordinate[1] + q )) is not None:
                current_hex.add_neighbour(self.hex_dict.get((current_hex.coordinate[0] + r , current_hex.coordinate[1] + q )))

'''
graph = Graph()
for i in graph.hex_dict.values():
    print("current hex is {a} and has neibour".format(a = i.coordinate))
    i.print_neighbour()
'''