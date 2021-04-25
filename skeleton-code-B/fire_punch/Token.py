# class Token will keep the information for one single token and also manage the move of this token.
class Token:

    # initialize a token with its type and coordinate.
    def __init__(self, coordinate, species):
        self.coordinate = coordinate
        self.type = species

    ''' 
    move a token from its current to the destination and check the movement is a slide or swing
    and print out the movement.
    '''

    def move(self, dest_coordinate, distance):
        self.coordinate = dest_coordinate

    '''
    if distance > 1:
            print('SWING from ({ax},{ay}) to ({bx},{by})'.format(ax=self.coordinate[0], ay=self.coordinate[1],
                                                                 bx=dest_coordinate[0], by=dest_coordinate[1]))

        else:
            print('SLIDE from ({ax},{ay}) to ({bx},{by})'.format(ax=self.coordinate[0], ay=self.coordinate[1],
                                                                 bx=dest_coordinate[0], by=dest_coordinate[1]))
        '''

    # check if the current token can defeat the input token.
    def defeat(self, enemy):
        if self.type == 'r' and enemy.type == 's':
            return True
        elif self.type == 's' and enemy.type == 'p':
            return True
        elif self.type == 'p' and enemy.type == 'r':
            return True
        else:
            return False
