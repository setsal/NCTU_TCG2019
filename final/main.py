#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""

from board import board
from game import game
from mcts import mcts
from enemy import enemy
import sys


def run():
    time = 9000
    for para in sys.argv[1:]:
        if "--time=" in para:
            time = int(para[(para.index("=") + 1):])
    try:
        """ Initial Board """
        myboard = board()
        mygame = game(myboard)

        """ create Enemy and AI """
        myboard.init_board()
        p1, p2 = myboard.players

        """ First Round  """
        myEnemy = enemy(player=p1)
        myAi = mcts(timeLimit=time, player=p2)
        signal = mygame.start(myEnemy, myAi)

        while(True):
            if  signal == "CLEAN":
                """ New Round """
                myboard.init_board()
                p1, p2 = myboard.players    #1, 2
                myEnemy = enemy(player=p1)
                myAi = mcts(timeLimit=time, player=p2)
                signal = mygame.start(myEnemy, myAi)
            elif signal == "END":
                break

    except KeyboardInterrupt:
        print("STOP")


if __name__ == "__main__":
    # print('NoGo Demo')
    run()
