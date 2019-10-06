#!/usr/bin/env python3

"""
Framework for threes  Games
Modified from  Hung Guei (moporgic) 2048 & 2048-like framework

Author: setsal Lan (setsal)
"""

from board import board
from action import action
import random


global operation
operation = -1

class agent:
    """ base agent """
    
    def __init__(self, options = ""):
        self.info = {}
        options = "name=unknown role=unknown " + options
        for option in options.split():
            data = option.split("=", 1) + [True]
            self.info[data[0]] = data[1]
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
        self.rstate = random.getstate()
        return
    
    def choice(self, seq):
        random.setstate(self.rstate)
        target = random.choice(seq)
        self.rstate = random.getstate()
        return target
    
    def shuffle(self, seq):
        random.setstate(self.rstate)
        random.shuffle(seq)
        self.rstate = random.getstate()
        return


class rndenv(random_agent):
    """
    random environment
    choic a random tile from threes bag
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
            # print("remain bag" + str(self.threes_bag ))

            """ Change to bag selection """
            if not self.threes_bag:
                self.threes_bag = [1,2,3]
            tile = self.choice(self.threes_bag)
            self.threes_bag.remove(tile)
            # print("Env put: " + str(tile) + ", in postion: " + str(pos))
            
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
            """   Simple choice strategy ---> Prefer Up and Right  """
            if 0 in legal:
                if 1 in legal:
                    op = self.choice([0,1])
                else:
                    op = 0
            elif 1 in legal:
                op = 1
            else:
                op = self.choice(legal)
            # print("Player do: " + str(self.res[op]))

            """ remember the current operation for current player doing """
            global operation
            operation = op

            return action.slide(op)
        else:
            return action()
    
    
if __name__ == '__main__':
    print('2048 Demo: agent.py\n')
    
    state = board()
    env = rndenv()
    ply = player()
    
    a = env.take_action(state)
    r = a.apply(state)
    print(a)
    print(r)
    print(state)
        
    a = env.take_action(state)
    r = a.apply(state)
    print(a)
    print(r)
    print(state)
    
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    
    state = board()
    state[0] = 1
    state[1] = 1
    print(state)
    
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(state)
    
