#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""

def negotiate(input):
    if input == "protocol_version":
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
