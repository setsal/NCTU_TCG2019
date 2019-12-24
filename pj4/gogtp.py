#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""

class gogtp:
    """
    Control Game State
    """

    def __init__(self, board):
        return

    def negotiate(self, input):
        if input == "protocol_version":
            print("=2")
            print("")

        elif input == "name":
            print("=0856016")
            print("")

        elif input in ["version", "list_commands", "final_score"]:
            print("=")
            print("")

        elif input == "clear_board":
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
            return "enemy: " + input.replace("play W ", "").replace("play B ", "")


if __name__ == "__main__":
    print("NoGO Demo: gogtp.py\n")
    pass

