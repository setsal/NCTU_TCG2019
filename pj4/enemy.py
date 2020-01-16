#!/usr/bin/env python3

"""
Framework for NoGo
Modified from  setsal Lan (setsal) NoGo framework

Author: setsal Lan (setsal)
"""

import random

class enemy:
    """
    enemy player
    """

    def __init__(self, player):
        self.player = player

    def __str__(self):
        return "Agent: {}".format(self.player)