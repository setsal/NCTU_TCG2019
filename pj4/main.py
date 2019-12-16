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
    try:
        """ Initial Board """
        myboard = board()
        mygame = game(myboard)

        """ create human and AI """
        myboard.init_board()
        p1, p2 = myboard.players

        myhuman = human(p1)
        # n in row, time, action
        ai = mcts(timeLimit=1000, player=p2)
        
        signal = mygame.start(myhuman, ai)
        while signal != "END":
                myboard.init_board()
                p1, p2 = myboard.players
                myhuman = human(p1)
                ai = mcts(timeLimit=1000, player=p2)
                signal = mygame.start(myhuman, ai)

    except KeyboardInterrupt:
        print('\n\rquit')

if __name__ == '__main__':
    # print('NoGo Demo: ' + " ".join(sys.argv))
    run()