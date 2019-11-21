
from enum import Enum

class Game():
    def choose(self, choice):
        raise NotImplementedError()

class Strategy():
    def __init__(self, p1_strat, p2_strat):
        try:
            iter(p1_strat)
        except TypeError as te:
            raise ValueError(f'{p1_strat} is not iterable')
        try:
            iter(p2_strat)
        except TypeError as te:
            raise ValueError(f'{p2_strat} is not iterable')
        self.P1_STRAT = p1_strat
        self.P2_STRAT = p2_strat
    def sample(self):
        raise NotImplementedError()

class Outcome():
    pass

class Player():
    def __init__(self, choices):
        raise NotImplementedError()
    def regret(self, choice, outcome):
        raise NotImplementedError()
    def utility(self, outcome):
        raise NotImplementedError()
    def get_choice(self):
        raise NotImplementedError()

class Choice(Enum):
    pass
