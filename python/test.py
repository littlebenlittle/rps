
import logging
import numpy as np
from rps import *

logging.basicConfig(filename='/dev/null', level=logging.DEBUG)

o = 0.0
l = 1.0
h = 0.5
ROCK     = (l,o,o)
PAPER    = (o,l,o)
SCISSORS = (o,o,l)
ROCK_PAPER     = (h,h,o)
ROCK_SCISSORS  = (h,o,h)
PAPER_SCISSORS = (o,h,h)

def approx_eq(a, b, tolerance):
    assert abs(a-b) < tolerance

class ConstantPlayer(RPSPlayer):
    def __init__(self, strategy):
        self.strategy = strategy

class RegretMatchingPlayer(RPSPlayer):
    def __init__(self, init_strategy=ROCK):
        super().__init__()
        self.strategy = init_strategy
        self.cumulative_regret = np.array([0, 0, 0])

    # TODO: this is not implemented 2019-11-20Z17:24:25
    def update_strategy(self, outcome):
        self.cumulative_regret += self.regret(outcome)

def test_regret_matcher():
    p1 = RegretMatchingPlayer()
    p2 = ConstantPlayer(ROCK)
    for _ in range(100):
        s = RPSStrategy(p1.strategy, p2.strategy)
        outcome = s.sample()
        p1.update_strategy(outcome)
    tolerance = 0.05
    logging.debug(f'strategy: {p1.cumulative_regret}')
    approx_eq(p1.strategy_for(RPSChoice.ROCK), 0., tolerance)
    approx_eq(p1.strategy_for(RPSChoice.PAPER), 1., tolerance)
    approx_eq(p1.strategy_for(RPSChoice.SCISSORS), 0., tolerance)

def test_rps_player_utility():
    p = RPSPlayer()
    assert p.utility(RPSOutcome(RPSChoice.ROCK, RPSChoice.SCISSORS)) == 1
    assert p.utility(RPSOutcome(RPSChoice.ROCK, RPSChoice.PAPER)) == -1
    assert p.utility(RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK)) == 0

def test_rps_player_regret():
    p = RPSPlayer()
    WIN  = RPSOutcome(RPSChoice.ROCK, RPSChoice.SCISSORS)
    LOSE = RPSOutcome(RPSChoice.ROCK, RPSChoice.PAPER)
    TIE  = RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK)
    assert p.regret(WIN)  == 0
    assert p.regret(LOSE) == 2
    assert p.regret(TIE)  == 1
