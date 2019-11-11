#!/usr/bin/env python3

"""
Framework for threes Games
Modified from  Hung Guei (moporgic) 2048 & 2048-like framework

Author: setsal Lan (setsal)
"""

from board import board
from action import action
global operation
operation = -1
from weight import weight
from array import array
import random
import sys



class agent:
    """ base agent """
    
    def __init__(self, options = ""):
        self.info = {}
        options = "name=unknown role=unknown " + options
        for option in options.split():
            data = option.split("=", 1) + [True]
            self.info[data[0]] = data[1]
        return
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        return
    
    def open_episode(self, flag = ""):
        return
    
    def close_episode(self, flag = ""):
        return
    
    def take_action(self, state):
        return action()
    
    def check_for_win(self, state):
        return False
    
    def property(self, key):
        return self.info[key] if key in self.info else None
    
    def notify(self, message):
        data = message.split("=", 1) + [True]
        self.info[data[0]] = data[1]
        return
    
    def name(self):
        return self.property("name")
    
    def role(self):
        return self.property("role")


class random_agent(agent):
    """ base agent for agents with random behavior """
    
    def __init__(self, options = ""):
        super().__init__(options)
        seed = self.property("seed")
        global operation
        operation = -1
        if seed is not None:
            random.seed(int(seed))
        return
    
    def choice(self, seq):
        target = random.choice(seq)
        return target
    
    def shuffle(self, seq):
        random.shuffle(seq)
        return
    
    
class weight_agent(agent):
    """ base agent for agents with weight tables """
    
    def __init__(self, options = ""):
        super().__init__(options)
        self.net = []
        init = self.property("init")
        if init is not None:
            self.init_weights(init)
        load = self.property("load")
        if load is not None:
            self.load_weights(load)
        return
    
    def __exit__(self, exc_type, exc_value, traceback):
        save = self.property("save")
        if save is not None:
            self.save_weights(save)
        return
    
    def init_weights(self, info):
        #self.net = [weight(65536)] * 8
        self.net = [weight(16777216)] * 32
        return

    def load_weights(self, path):
        input = open(path, 'rb')
        size = array('L')
        size.fromfile(input, 1)
        size = size[0]
        for i in range(size):
            self.net += [weight()]
            self.net[-1].load(input)
        return
    
    def save_weights(self, path):
        output = open(path, 'wb')
        array('L', [len(self.net)]).tofile(output)
        for w in self.net:
            w.save(output)
        return


class learning_agent(weight_agent):
    """ base agent for agents with a learning rate """
    
    res = [ "#U", "#R", "#D", "#L", "#?" ]

    def __init__(self, options = ""):
        super().__init__(options)
        self.alpha = 0.1
        self.last_state = None
        self.last_value = 0
        self.first = False
        self.tuplesPos = [
                [ 0, 1, 2, 3, 4, 5 ],[ 3, 7, 11, 15, 2, 6 ],[ 15, 14, 13, 12, 11, 10 ],[ 12, 8, 4, 0, 13, 9 ],
                [ 3, 2, 1, 0, 7, 6 ],[ 0, 4, 8, 12, 1, 5 ],[ 12, 13, 14, 15, 8, 9 ],[ 15, 11, 7, 3, 14, 10 ],
                [ 4, 5, 6, 7, 8, 9 ],[ 2, 6, 10, 14, 1, 5 ],[ 11, 10, 9, 8, 7, 6 ],[ 13, 9, 5, 1, 14, 10 ],
                [ 7, 6, 5, 4, 11, 10 ],[ 1, 5, 9, 13, 2, 6 ],[ 8, 9, 10, 11, 4, 5 ],[ 14, 10, 6, 2, 13, 9 ],
                [ 0, 1, 2, 4, 5, 6 ],[ 3, 7, 11, 2, 6, 10 ],[ 15, 14, 13, 11, 10, 9 ],[ 12, 8, 4, 13, 9, 5 ],
                [ 3, 2, 1, 7, 6, 5 ],[ 0, 4, 8, 1, 5, 9 ],[ 12, 13, 14, 8, 9, 10 ],[ 15, 11, 7, 14, 10, 6 ],
                [ 4, 5, 6, 8, 9, 10 ],[ 2, 6, 10, 1, 5, 9 ],[ 11, 10, 9, 7, 6, 5 ], [ 13, 9, 5, 14, 10, 6 ], 
                [ 7, 6, 5, 11, 10, 9 ], [ 1, 5, 9, 2, 6, 10 ], [ 8, 9, 10, 4, 5, 6 ], [ 14, 10, 6, 13, 9, 5 ]
        ]
        alpha = self.property("alpha")
        if alpha is not None:
            self.alpha = float(alpha)
        return
    
    def open_episode(self, flag = ""):
        self.first = True

    def recoverOp(self):
        global operation
        operation = -1
        return

    """ calculate function """
    def encode(self, state, target):
        return ( state[target[0]] << 0 ) | ( state[target[1]] << 4 ) | ( state[target[2]] << 8 ) | ( state[target[3]] << 12 ) | ( state[target[4]] << 16 ) | ( state[target[5]] << 20 )

    """ board state"""
    def evaluate(self, state):
        v = 0
        for i in range(32):
            v += self.net[i][self.encode(state.state, self.tuplesPos[i])]
        return v        

    """ board state,  float target"""
    def update(self, state, target):
        v = ( self.alpha / 32 ) * ( target - self.evaluate(state) )
        for i in range(32):
            self.net[i][self.encode(state.state, self.tuplesPos[i])] += v
        return

    """ board before """
    def take_action(self, before):
        best_value = -1000000
        best_action = None
        
        for op in range(4):
            after = board(before)
            reward = after.slide(op)
            if reward != -1:
                v = reward + self.evaluate(after)
                if v > best_value:
                    best_value = v
                    best_action = action.slide(op)
                    global operation
                    operation = op
        
        if not self.first:
            if best_value != -1000000:
                self.update(self.last_state, best_value)
            else:
                self.update(self.last_state, 0)

        self.last_state = board(before)
        self.last_state.slide(operation)
        self.last_value = self.evaluate(self.last_state)
        self.first = False

        if best_action == None:
            return action()
        else:
            return best_action

class rndenv(random_agent):
    """
    random environment
    add a new random tile to an empty cell
    2-tile: 90%
    4-tile: 10%
    """
    threes_bag = [1, 2, 3]
    
    def __init__(self, options = ""):
        super().__init__("name=random role=environment " + options)
        return

    def recoverBag(self):
        self.threes_bag = [1,2,3]
        return

    def take_action(self, state):
        """ Get the last player operation """
        global operation
        # print('Get player operation:' + str(operation) ) 
        if operation == 0:
            #UP
            empty = [pos for pos, tile in enumerate(state.state) if not tile and pos in [12,13,14,15]]
        elif operation == 1:
            #Right
            empty = [pos for pos, tile in enumerate(state.state) if not tile and pos in [0,4,8,12] ]
        elif operation == 2:
            #Down
            empty = [pos for pos, tile in enumerate(state.state) if not tile and pos in [0,1,2,3] ]
        elif operation == 3:
            #Left
            empty = [pos for pos, tile in enumerate(state.state) if not tile and pos in [3,7,11,15]]
        else:
            empty = [pos for pos, tile in enumerate(state.state) if not tile]
        
        if empty:
            pos = self.choice(empty)
            """ Change to bag selection """
            if not self.threes_bag:
                self.threes_bag = [1,2,3]
            tile = self.choice(self.threes_bag)
            self.threes_bag.remove(tile)
            return action.place(pos, tile)
        else:     
            return action()
    
    
class player(random_agent):
    """
    dummy player
    select a legal action randomly
    """
    res = [ "#U", "#R", "#D", "#L", "#?" ]    
    
    def __init__(self, options = ""):
        super().__init__("name=dummy role=player " + options)
        return
    
    def recoverOp(self):
        global operation
        operation = -1
        return

    def take_action(self, state):
        legal = [op for op in range(4) if board(state).slide(op) != -1]
        if legal:
            op = self.choice(legal)

            """ remember the current operation for current player doing """
            global operation
            operation = op

            return action.slide(op)
        else:
            return action()
    
    
if __name__ == '__main__':
    print('Threes Demo: agent.py\n')
    pass
