#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""
from copy import deepcopy
import time
from random import choice, shuffle
from math import log, sqrt

class board:
    """
    board for game
    """

    def __init__(self):
        self.width = 9
        self.states = {} # board states, key:move, value: player as piece type
        self.players = [1, 2]  # player1 and player2        

    def init_board(self):
        self.current_player = self.players[0]  # start player
        self.availables = {}
        for player in self.players:
            self.availables[player] = list(range(self.width * self.width))

        self.states = {} # key:move as location on the board, value:player as pieces type
        self.last_move = -1

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move  // self.width
        w = move  %  self.width
        return [h, w]

    def location_to_move(self, location):
        if(len(location) != 2):
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if(move not in range(self.width * self.width)):
            return -1
        return move
    
    def getPossibleActions(self, player):
        return self.availables[player] 
        
    def is_movable(self, move, player):
        if move in self.states: return False
        if move >= self.width * self.width: return False
        if move < 0: return False

        # do not lock other player
        other_player = self.get_other_player(player)
        for adj_move in self.adjacent_moves(move):
            if adj_move in self.states and self.states[adj_move] == other_player:
                visited = [0] * (self.width * self.width )
                visited[move] = 1
                if not self.has_vacancy(adj_move, visited):
                    return False

        # do not block current player
        for adj_move in self.adjacent_moves(move):
            if adj_move not in self.states:
                return True

        visited = [0] * (self.width * self.width)
        visited[move] = 1

        for adj_move in self.adjacent_moves(move):
            if adj_move in self.states and self.states[adj_move] == player:
                if self.has_vacancy(adj_move, visited):
                    return True

        return False

    def adjacent_moves(self, move):
        h, w = self.move_to_location(move)
        adjs = []
        if h > 0: adjs.append(self.location_to_move((h-1, w)))
        if h < self.width - 1: adjs.append(self.location_to_move((h+1, w)))
        if w > 0: adjs.append(self.location_to_move((h, w-1)))
        if w < self.width - 1: adjs.append(self.location_to_move((h, w+1)))
        return adjs

    def has_vacancy(self, move, visited):
        if visited[move] == 1: return False
        visited[move] = True

        for adj_move in self.adjacent_moves(move):
            if visited[adj_move] == 1: continue
            if adj_move not in self.states:
                return True
            if self.states[adj_move] == self.states[move]:
                if self.has_vacancy(adj_move, visited):
                    return True
        return False

    def update(self,move):
        self.states[move] = self.current_player
        self.current_player = self.get_other_player(self.current_player)
        self.last_move = move

        # 由於已經下了, 刪除雙方的 availables locations
        for player in self.players:
            if move in self.availables[player]:
                self.availables[player].remove(move)

        # 調整雙方目前狀態之 availables 
        for player in self.players:
            trash = []
            for can_move in self.availables[player]:
                if not self.is_movable(can_move, player):
                    trash.append(can_move)
            
            # 刪除不可走之步
            for can_move in trash:
                self.availables[player].remove(can_move)

    def get_current_player(self):
        return self.current_player

    def get_other_player(self, player):
        return self.players[0] if player==self.players[1]  else self.players[1]

    def current_state(self):
        return tuple((m, self.states[m]) for m in sorted(self.states)) # for hash

    def getReward(self, player):
        if len(self.availables[player]) == 0:
            return 1
        else:
            return 0


    def takeAction(self, action, player):
        newState = deepcopy(self)
        newState.update(action)
        newState.currentPlayer = 1 if player == 2 else 2
        return newState

    def isTerminal(self):
        """Check whether the game is ended or not"""
        if len(self.availables[self.current_player]) == 0:
            return True
        else:
            return False
    
if __name__ == '__main__':
    # print('NoGO Demo: board.py\n')
    pass
