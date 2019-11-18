
import logging
from rps import *

logging.basicConfig(filename='/dev/null', level=logging.DEBUG)

def approx_eq(a, b, tolerance):
    r = abs(a-b) < tolerance
    #logging.debug(f' |{a} - {b}| < {tolerance} : {r}')
    return r

def test_rps_player_utility():
    t = 0.05  # tolerance
    ROCK     = (1.,0.,0.)
    PAPER    = (0.,1.,0.)
    SCISSORS = (0.,0.,1.)
    p = RPSPlayer()
    u = p.utility(RPSStrategy(ROCK, ROCK))
    assert approx_eq(u, 0., t)
    u = p.utility(RPSStrategy(ROCK, PAPER))
    assert approx_eq(u, -1., t)
    u = p.utility(RPSStrategy(ROCK, SCISSORS))
    assert approx_eq(u, 1., t)

def test_rps_player_regret():
    p = RPSPlayer()
    assert p.regret(RPSChoice.ROCK, RPSOutcome.WIN) == (0, 0, 0)
    assert p.regret(RPSChoice.PAPER, RPSOutcome.WIN) == (0, 0, 0)
    assert p.regret(RPSChoice.SCISSORS, RPSOutcome.WIN) == (0, 0, 0)
    assert p.regret(RPSChoice.ROCK, RPSOutcome.TIE) == (0, 1, 0)
    assert p.regret(RPSChoice.PAPER, RPSOutcome.TIE) == (0, 0, 1)
    assert p.regret(RPSChoice.SCISSORS, RPSOutcome.TIE) == (1, 0, 0)
    assert p.regret(RPSChoice.ROCK, RPSOutcome.LOSE) == (0, 1, 2)
    assert p.regret(RPSChoice.PAPER, RPSOutcome.LOSE) == (2, 0, 1)
    assert p.regret(RPSChoice.SCISSORS, RPSOutcome.LOSE) == (1, 2, 0)

def test_rps_outcome():
    assert get_outcome(RPSChoice.ROCK, RPSChoice.ROCK) is RPSOutcome.TIE
    assert get_outcome(RPSChoice.ROCK, RPSChoice.PAPER) is RPSOutcome.LOSE
    assert get_outcome(RPSChoice.ROCK, RPSChoice.SCISSORS) is RPSOutcome.WIN
    assert get_outcome(RPSChoice.PAPER, RPSChoice.ROCK) is RPSOutcome.WIN
    assert get_outcome(RPSChoice.PAPER, RPSChoice.PAPER) is RPSOutcome.TIE
    assert get_outcome(RPSChoice.PAPER, RPSChoice.SCISSORS) is RPSOutcome.LOSE
    assert get_outcome(RPSChoice.SCISSORS, RPSChoice.ROCK) is RPSOutcome.LOSE
    assert get_outcome(RPSChoice.SCISSORS, RPSChoice.PAPER) is RPSOutcome.WIN
    assert get_outcome(RPSChoice.SCISSORS, RPSChoice.SCISSORS) is RPSOutcome.TIE
