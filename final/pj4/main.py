#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""

from board import board
from game import game
from mcts import mcts
from human import human
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

        """ create human and AI """
        myboard.init_board()
        p1, p2 = myboard.players

        myhuman = human(p1)
        # n in row, time, action
        ai = mcts(timeLimit=time, player=p2)

        signal = mygame.start(myhuman, ai)
        while signal != "END":
            myboard.init_board()
            p1, p2 = myboard.players
            myhuman = human(p1)
            ai = mcts(timeLimit=time, player=p2)
            signal = mygame.start(myhuman, ai)

    except KeyboardInterrupt:
        print("STOP")


if __name__ == "__main__":
    # print('NoGo Demo')
    run()
