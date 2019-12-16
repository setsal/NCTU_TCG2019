import random

class human:
    """
    human player
    """
    def __init__(self, player):
        self.player = player

    def get_action(self, board): 
        print("[*] For Player: {p} -> {q}".format(p=self.player, q=board.availables[self.player]))
        move = random.choice(list(board.availables[self.player]))
        print("[*] Choose {}".format(move))

        return move

    def __str__(self):
        return "Agent: {}".format(self.player)