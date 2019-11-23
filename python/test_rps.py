
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

def test_RPSStrategy_sample():
    p1 = ConstantPlayer(ROCK)
    p2 = ConstantPlayer(ROCK)
    s = RPSStrategy(p1.strategy, p2.strategy)
    outcome = s.sample()
    assert outcome == RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK)

def test_RPSPlayer_utility():
    p = RPSPlayer()
    assert p.utility(ROCK_SCISSORS_OUTCOME) == 1
    assert p.utility(ROCK_PAPER_OUTCOME) == -1
    assert p.utility(ROCK_ROCK_OUTCOME) == 0
    assert all(p.utility([
        ROCK_SCISSORS_OUTCOME,
        ROCK_PAPER_OUTCOME,
        ROCK_ROCK_OUTCOME
    ]) == np.array([1,-1,0]))

def test_RPSPlayer_regret():
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

def test_RegretMatchingPlayer():
    for p2_strat, p1_opt_strat in (
                (ROCK, PAPER),
                (PAPER, SCISSORS),
                (SCISSORS, ROCK),
                (NASHEQ, NASHEQ),
            ):
        p1 = RegretMatchingPlayer()
        p2 = ConstantPlayer(p2_strat)
        for _ in range(1000):
            s = RPSStrategy(p1.strategy, p2.strategy)
            outcome = s.sample()
            p1.update_strategy(outcome)
        tolerance = 0.05
        approx_eq(p1.strategy, p1_opt_strat, tolerance)

def test_RegretMatchingPlayer_update_strategy():
    p1 = RegretMatchingPlayer(blind_strategy=ROCK)
    p2 = ConstantPlayer(ROCK)
    s = RPSStrategy(p1.strategy, p2.strategy)
    outcome = s.sample()
    p1.update_strategy(outcome)
    assert all(p1.cumulative_regret == np.array([0,1,0]))
    assert all(p1.strategy == np.array([0.,1.,0.]))

