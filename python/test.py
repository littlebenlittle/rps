
import logging
import numpy as np
from rps import *

logging.basicConfig(filename='/dev/null', level=logging.DEBUG)

ROCK     = np.array([1.,0.,0.])
PAPER    = np.array([0.,1.,0.])
SCISSORS = np.array([0.,0.,1.])
NASHEQ   = np.array([1.,1.,1.]) / 3.

ROCK_ROCK_OUTCOME         = RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK)
ROCK_PAPER_OUTCOME        = RPSOutcome(RPSChoice.ROCK, RPSChoice.PAPER)
ROCK_SCISSORS_OUTCOME     = RPSOutcome(RPSChoice.ROCK, RPSChoice.SCISSORS)
PAPER_ROCK_OUTCOME        = RPSOutcome(RPSChoice.PAPER, RPSChoice.ROCK)
PAPER_PAPER_OUTCOME       = RPSOutcome(RPSChoice.PAPER, RPSChoice.PAPER)
PAPER_SCISSORS_OUTCOME    = RPSOutcome(RPSChoice.PAPER, RPSChoice.SCISSORS)
SCISSORS_ROCK_OUTCOME     = RPSOutcome(RPSChoice.SCISSORS, RPSChoice.ROCK)
SCISSORS_PAPER_OUTCOME    = RPSOutcome(RPSChoice.SCISSORS, RPSChoice.PAPER)
SCISSORS_SCISSORS_OUTCOME = RPSOutcome(RPSChoice.SCISSORS, RPSChoice.SCISSORS)

def approx_eq(a, b, tolerance):
    assert all(abs(a-b) < tolerance)

class ConstantPlayer(RPSPlayer):
    def __init__(self, strategy):
        self.strategy = strategy

class RegretMatchingPlayer(RPSPlayer):
    def __init__(self, blind_strategy=NASHEQ):
        super().__init__()
        self.strategy = blind_strategy
        self.cumulative_regret = np.array([0, 0, 0])

    def update_strategy(self, outcome):
        self.cumulative_regret += self.regret(outcome)
        total_regret = self.cumulative_regret.sum()
        if total_regret == 0:
            self.strategy = NASHEQ
            return
        self.strategy = self.cumulative_regret / total_regret

def test_RegretMatchingPlayer():
    p1 = RegretMatchingPlayer(blind_strategy=ROCK)
    p2 = ConstantPlayer(ROCK)
    for _ in range(100):
        s = RPSStrategy(p1.strategy, p2.strategy)
        outcome = s.sample()
        p1.update_strategy(outcome)
    tolerance = 0.05
    logging.debug(f'regret: {p1.cumulative_regret}')
    logging.debug(f'strategy: {p1.strategy}')
    approx_eq(p1.strategy, PAPER, tolerance)

def test_RegretMatchingPlayer_update_strategy():
    p1 = RegretMatchingPlayer(blind_strategy=ROCK)
    p2 = ConstantPlayer(ROCK)
    s = RPSStrategy(p1.strategy, p2.strategy)
    outcome = s.sample()
    p1.update_strategy(outcome)
    assert all(p1.cumulative_regret == np.array([0,1,0]))
    assert all(p1.strategy == np.array([0.,1.,0.]))

def test_RPSStrategy_sample():
    p1 = ConstantPlayer(ROCK)
    p2 = ConstantPlayer(ROCK)
    s = RPSStrategy(p1.strategy, p2.strategy)
    outcome = s.sample()
    assert outcome == RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK)

def test_rps_player_utility():
    p = RPSPlayer()
    assert p.utility(ROCK_SCISSORS_OUTCOME) == 1
    assert p.utility(ROCK_PAPER_OUTCOME) == -1
    assert p.utility(ROCK_ROCK_OUTCOME) == 0
    assert all(p.utility([
        ROCK_SCISSORS_OUTCOME,
        ROCK_PAPER_OUTCOME,
        ROCK_ROCK_OUTCOME
    ]) == np.array([1,-1,0]))

def test_rps_player_regret():
    p = RPSPlayer()
    # wins:
    assert all(p.regret(ROCK_SCISSORS_OUTCOME)     == np.array([0,0,0]))
    assert all(p.regret(PAPER_ROCK_OUTCOME)        == np.array([0,0,0]))
    assert all(p.regret(SCISSORS_PAPER_OUTCOME)    == np.array([0,0,0]))
    # ties:
    assert all(p.regret(SCISSORS_SCISSORS_OUTCOME) == np.array([1,0,0]))
    assert all(p.regret(ROCK_ROCK_OUTCOME)         == np.array([0,1,0]))
    assert all(p.regret(PAPER_PAPER_OUTCOME)       == np.array([0,0,1]))
    # losses
    assert all(p.regret(ROCK_PAPER_OUTCOME)        == np.array([0,1,2]))
    assert all(p.regret(PAPER_SCISSORS_OUTCOME)    == np.array([2,0,1]))
    assert all(p.regret(SCISSORS_ROCK_OUTCOME)     == np.array([1,2,0]))
