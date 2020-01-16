#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""
from __future__ import print_function
import copy
import time
from random import choice, shuffle
import sys
from math import log, sqrt
from mcts import mcts
from human import human

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class game:
    """
    Control Game State
    """

    def __init__(self, board):
        self.board = board
        self.time = float(15)
        self.max_actions = int(1000)

    def negotiate(self, input):
        if input == "protocol_version":
            eprint("[*] SEND COMMAND: " + "=2" )
            print("=2")
            print("")
            return "none"
        elif input == "name":
            print("=0856016")
            print("")
            return "none"
        elif input in ["version", "list_commands", "final_score"]:
            print("=")
            print("")
            return "none"
        elif input.startswith("boardsize"):
            print("=")
            print("")
            return "none"
        elif input == "clear_board":
            print("=")
            print("")
            return "clean"
        elif input == "=resign":
            print("!!!ENEMY RESIGN!!!!")
            print("=")
            print("")
            return "clean"
        elif input == "quit":
            return "quit"
        elif input.startswith("genmove"):
            return "move"
        elif input.startswith("play"):
            print("=")
            print("")
            return "enemy:" + input.replace("play W ", "").replace("play B ", "")
        else:
            print("Invalid Argument!!!???")
            return "!!!!Invalid Enemy Argument!!!!" + input

    def start(self, player1, player2):
        p1, p2 = self.board.players
        players = {}
        players[p1] = player1
        players[p2] = player2

        # self.graphic(self.board, player1, player2)
        # print('------- Game Start ---------')
        while True:
            enemy_input = input()
            eprint("[*] GET ENEMY INPUT: " + enemy_input )
            motion = self.negotiate(enemy_input)

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
                # print("[*] My AI turn !" )
                move = players[2].get_action(self.board)
                res = self.board.move_to_location(move)
                ans = "=" + chr(res[1] + ord("A")) + chr(res[0] + ord("1"))
                print(ans)
                print("")
                self.board.update(move)
            elif motion.startswith("enemy:"):
                # print("[*] Enemy Turn !")
                location = [
                    ord(motion[6:][1]) - ord("1"),
                    ord(motion[6:][0]) - ord("A"),
                ]  # 1, A
                move = self.board.location_to_move(location)
                if move not in self.board.getPossibleActions(2):
                    print("!!!$$$ ENEMY INVALID MOVE, Keep continue will let this round false  $$$!!!!")
                self.board.update(move)

            # print("[*] Choose {} to move".format(move))
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


if __name__ == "__main__":
    print("NoGO Demo: game.py\n")
    pass

