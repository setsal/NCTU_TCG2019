from __future__ import division

import copy
import time
from random import choice, shuffle
from math import log, sqrt

import time
import math
import random


def randomPolicy(state):
    # print("In random Policy:")
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions(state.current_player))
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action, state.current_player)
    return state.getReward(state.current_player)


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts:
    def __init__(self, timeLimit=None, iterationLimit=1000, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy, player=1):
        # set player
        self.player = player
        self.timeLimit = timeLimit
        self.limitType = 'time'

        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)
        
        timeLimit = time.time() + self.timeLimit / 1000
        while time.time() < timeLimit:
            self.executeRound()

        # When over the time limit, get the best child
        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        # print("Get reward" + str(reward))
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        player = node.state.get_current_player()
        actions = node.state.getPossibleActions(player)
        
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action,player), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action

    def get_action(self, board):
        move = self.search(initialState=board)
        return move

if __name__ == '__main__':
    # print('NoGO Demo: mcts.py\n')
    pass 