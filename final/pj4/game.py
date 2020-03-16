#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""
from __future__ import print_function
import sys
from mcts import mcts
import random
import gogtp

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class game:
    """
    Control Game State
    """

    def __init__(self, board):
        self.board = board
        self.time = 0

    def start(self, player1, player2):
        p1, p2 = self.board.players   #get 1, 2
        players = {}
        black = [  38, 30, 40, 32, 42, 34, 44, 54, 46, 56, 48, 58, 50, 60, 52, 62, 72, 64, 74, 66, 76, 68, 78, 70, 80 ]
        # random.shuffle(black)

        """ 設定角色 """
        players[p1] = player1    # Enemy
        players[p2] = player2    # AI

        # self.graphic(self.board, player1, player2)
        # print('------- Game Start ---------')
        while True:
            self.time = self.time + 1
            gogtp_input = input()
            motion = gogtp.negotiate(gogtp_input)

            if motion == "none":
                continue
            elif motion == "quit":
                return "END"
            elif motion == "clean":
                return "CLEAN"
            elif motion == "move":
                if self.board.isTerminal():
                    print("=resign")
                    print("")
                    break

                """ AI Move """

                """ add a little trick """
                if len(black) != 0:
                    move = black.pop()
                    eprint("[*] black move!?" + str(move) )
                    if move in self.board.availables[2]:
                        res = self.board.move_to_location(move)
                        if res[1] == 8: res[1] = res[1]+1 # FOR GTP..
                        print("=" + chr(res[1] + ord('A')) + chr(res[0] + ord('1')))
                        print("")                        
                        self.board.current_player = 2 # AI Current Play
                        self.board.update(move)
                    else:
                        move = players[p2].get_action(self.board)
                        eprint("[*] move!?" + str(move) )
                        res = self.board.move_to_location(move)
                        if res[1] == 8: res[1] = res[1]+1 # FOR GTP..
                        print("=" + chr(res[1] + ord('A')) + chr(res[0] + ord('1')))
                        print("")
                        self.board.current_player = 2 # AI Current Play
                        self.board.update(move)
                else:
                        move = players[p2].get_action(self.board)
                        eprint("[*] move!?" + str(move) )
                        res = self.board.move_to_location(move)
                        if res[1] == 8: res[1] = res[1]+1 # FOR GTP..
                        print("=" + chr(res[1] + ord('A')) + chr(res[0] + ord('1')))
                        print("")
                        self.board.current_player = 2 # AI Current Play
                        self.board.update(move)                    
                # self.graphic(self.board, player1, player2)

            elif motion.startswith("enemy:"):
                if motion[6:][0] == 'J':
                    """ ENEMY Move """
                    location = [
                        ord(motion[6:][1]) - ord('1'),
                        8,
                    ]  # A1 -> 1, A  -> ( 0, 0 )
                else:
                    """ ENEMY Move """
                    location = [
                        ord(motion[6:][1]) - ord('1'),
                        ord(motion[6:][0]) - ord('A'),
                    ]  # A1 -> 1, A  -> ( 0, 0 )
                
                move = self.board.location_to_move(location)
                if move not in self.board.availables[1]:
                    print("!!!$$$ ENEMY INVALID MOVE, STOP playing  $$$!!!")
                    exit(0)
                else:
                    self.board.current_player = 1 # Enemy Current Play
                    self.board.update(move)
                    # self.graphic(self.board, player1, player2)

            # Update move
        return "CLEAN"

    def game_end(self, ai):
        win, winner = ai.has_a_winner(self.board)
        if win:
            return True, winner
        elif not len(self.board.availables):
            print("Game end. Tie")
            return True, -1
        return False, -1


    def graphic(self, board, enemy, ai):
        """
        Draw the board and show game info
        """
        width = board.width

        eprint("Enemy Player", enemy.player, "with O".rjust(3))
        eprint("AI    Player", ai.player, "with X".rjust(3))
        eprint()
        for x in range(width):
            eprint("{0:4}".format(x), end='')
        eprint('\r\n')
        for i in range(width - 1, -1, -1):
            eprint("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == enemy.player:
                    eprint('O'.center(4), end='')
                elif p == ai.player:
                    eprint('X'.center(4), end='')
                else:
                    eprint('_'.center(4), end='')
            eprint('\r\n\r\n')


if __name__ == "__main__":
    print("NoGO Demo: game.py\n")
    pass

