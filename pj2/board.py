#!/usr/bin/env python3

"""
Framework for threes  Games
Modified from  Hung Guei (moporgic) 2048 & 2048-like framework

Author: setsal Lan (setsal)
"""

class board:
    """ simple implementation of threes puzzle """
    threes_seq = [ 0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144]
    
    def __init__(self, state = None):
        self.state = state[:] if state is not None else [0] * 16
        return
    
    def __getitem__(self, pos):
        return self.state[pos]
    
    def __setitem__(self, pos, tile):
        self.state[pos] = tile
        return
    
    def place(self, pos, tile):
        """
        place a tile (index value) to the specific position (1-d form index)
        return 0 if the action is valid, or -1 if not
        """
        if pos >= 16 or pos < 0:
            return -1
        if tile != 1 and tile != 2 and tile != 3:
            return -1
        self.state[pos] = tile
        return 0
    
    def slide(self, opcode):
        """
        apply an action to the board
        return the reward of the action, or -1 if the action is illegal
        """
        if opcode == 0:
            return self.slide_up()
        if opcode == 1:
            return self.slide_right()
        if opcode == 2:
            return self.slide_down()
        if opcode == 3:
            return self.slide_left()
        return -1
    
    def slide_left(self):
        move, score = [], 0
        for row in [self.state[r:r + 4] for r in range(0, 16, 4)]:
            if row[0] == 0:
                # Do nothing, just shift
                row = row[1:] + [0]
            elif row[0] == row[1] and row[0] != 1 and row[0] != 2:
                # normal add
                row[0] = row[0] + 1
                row[1:] = row[2:] + [0]
            elif row[0]+row[1] == 3 and row[1] != 0:
                # Do 1+2 = 3
                row[0] = 3
                row[1:] = row[2:] + [0]
            else:
                # row[0]!=row[1], check second move
                if row[1] == 0:
                    # Do nothing, just shift
                    row[1:] = row[2:] + [0]
                elif row[1] == row[2] and row[1] != 1 and row[1] != 2:
                    row[1] = row[1] + 1
                    row[2:] = row[3:] + [0]
                elif row[1]+row[2] == 3 and row[2] != 0:
                    # Do 1+2 = 3
                    row[1] = 3
                    row[2:] = row[3:] + [0]
                else:
                    if row[2] == 0:
                        # Do nothing, just shift
                        row[2:] = row[3:] + [0]
                    elif row[2] == row[3] and row[2] != 1 and row[2] != 2:
                        row[2] = row[2] + 1
                        row[3:] = row[4:] + [0]
                    elif row[2]+row[3] == 3 and row[3] != 0:
                        # Do 1+2 = 3
                        row[2] = 3
                        row[3:] = row[4:] + [0]
            move += row
        if move != self.state:
            self.state = move
            return score
        return -1
    
    def slide_right(self):
        self.reflect_horizontal()
        score = self.slide_left()
        self.reflect_horizontal()
        return score
    
    def slide_up(self):
        self.transpose()
        score = self.slide_left()
        self.transpose()
        return score
    
    def slide_down(self):
        self.transpose()
        score = self.slide_right()
        self.transpose()
        return score
    
    def reflect_horizontal(self):
        self.state = [self.state[r + i] for r in range(0, 16, 4) for i in reversed(range(4))]
        return
    
    def reflect_vertical(self):
        self.state = [self.state[c + i] for c in reversed(range(0, 16, 4)) for i in range(4)]
        return
    
    def transpose(self):
        self.state = [self.state[r + i] for i in range(4) for r in range(0, 16, 4)]
        return
    
    def rotate(self, rot = 1):
        rot = ((rot % 4) + 4) % 4
        if rot == 1:
            self.rotate_right()
            return
        if rot == 2:
            self.reverse()
            return
        if rot == 3:
            self.rotate_left()
            return
        return
    
    def rotate_right(self):
        """ clockwise rotate the board """
        self.transpose()
        self.reflect_horizontal()
        return
    
    def rotate_left(self):
        """ counterclockwise rotate the board """
        self.transpose()
        self.reflect_vertical()
        return
    
    def reverse(self):
        self.reflect_horizontal()
        self.reflect_vertical()
        return
        
    def __str__(self):
        # NEED judege
        state = '+' + '-' * 24 + '+\n'
        for row in [self.state[r:r + 4] for r in range(0, 16, 4)]:
            state += ('|' + ''.join('{0:6d}'.format(self.threes_seq[int(t)]) for t in row) + '|\n')
        state += '+' + '-' * 24 + '+'
        return state
    
    
if __name__ == '__main__':
    print('Threes Demo: board.py\n')
    
    state = board()
    state[0] = 2
    state[1] = 4
    state[2] = 2
    state[3] = 1
    # state[4] = 1
    # state[5] = 1
    # state[14] = 5
    print(state)
    state.slide_left()
    # state[10] = 10
    print(state)
