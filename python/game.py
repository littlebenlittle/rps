
from enum import Enum

class Game():
    def send_p1_move(self, move):
        raise NotImplementedError()
    def send_p2_move(self, move):
        raise NotImplementedError()
    def get_state(self):
        raise NotImplementedError()

class Player():
    def select_move(self, game_state):
        raise NotImplementedError()

class Strategy():
    def __init__(self, p1_strat, p2_strat):
        try:
            iter(p1_strat)
        except TypeError:
            raise ValueError(f'{p1_strat} is not iterable')
        try:
            iter(p2_strat)
        except TypeError:
            raise ValueError(f'{p2_strat} is not iterable')
        self.P1_STRAT = p1_strat
        self.P2_STRAT = p2_strat
    def sample(self):
        raise NotImplementedError()

class Outcome():
    pass

class Choice(Enum):
    pass
