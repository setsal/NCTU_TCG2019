#!/usr/bin/env python3

"""
Framework for threes  Games
Modified from  Hung Guei (moporgic) 2048 & 2048-like framework

Author: setsal Lan (setsal)
"""

from board import board
from action import action
from episode import episode
from statistic import statistic
from agent import player
from agent import rndenv
import sys


if __name__ == '__main__':
    print('Threes Demo: ' + " ".join(sys.argv))
    print()
    
    total, block, limit = 1000, 0, 0
    play_args, evil_args = "", ""
    load, save = "", ""
    summary = False
    for para in sys.argv[1:]:
        if "--total=" in para:
            total = int(para[(para.index("=") + 1):])
        elif "--block=" in para:
            block = int(para[(para.index("=") + 1):])
        elif "--limit=" in para:
            limit = int(para[(para.index("=") + 1):])
        elif "--play=" in para:
            play_args = para[(para.index("=") + 1):]
        elif "--evil=" in para:
            evil_args = para[(para.index("=") + 1):]
        elif "--load=" in para:
            load = para[(para.index("=") + 1):]
        elif "--save=" in para:
            save = para[(para.index("=") + 1):]
        elif "--summary" in para:
            summary = True
    
    stat = statistic(total, block, limit)
    
    if load:
        input = open(load, "r")
        stat.load(input)
        input.close()
        summary |= stat.is_finished()
    
    play = player(play_args)
    evil = rndenv(evil_args)
    
    while not stat.is_finished():
        play.open_episode("~:" + evil.name())
        evil.open_episode(play.name() + ":~")
        play.recoverOp()
        evil.recoverBag()
        stat.open_episode(play.name() + ":" + evil.name())
        game = stat.back()
        while True:
            # print(game.state())
            # print("Round end!")
            # print('')
            # if game.step() == 9:
            #         print("======= GAME start! ======= ")
            #         print('')            
            # print('[' + str(game.step()) + '] ')
            who = game.take_turns(play, evil)
            move =  who.take_action(game.state())
            if not game.apply_action(move) or who.check_for_win(game.state()):
                break
        win = game.last_turns(play, evil)
        stat.close_episode(win.name())
        
        play.close_episode(win.name())
        evil.close_episode(win.name())
    
    if summary:
        stat.summary()
    
    if save:
        output = open(save, "w")
        stat.save(output)
        output.close()
    
        