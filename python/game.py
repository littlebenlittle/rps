
from enum import Enum

class Game():
    def choose(self, choice):
        raise NotImplementedError()

class Strategy():
    P1_STRAT = None
    P2_STRAT = None
    def __init__(self, p1_strat, p2_strat):
        self.P1_STRAT = p1_strat
        self.P2_STRAT = p2_strat
    def sample(self):
        raise NotImplementedError()

class Outcome(Enum):
    pass

class Player():
    def regret(self, choice, outcome):
        raise NotImplementedError()
    def utility(self, outcome):
        raise NotImplementedError()

class Choice(Enum):
    pass
