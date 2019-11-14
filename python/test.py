
import rps


def test_sample_choice():
    num_samples = 10000
    strat = [0.3, 0.25, 0.45]
    choices = [rps.sample_choice(strat) for _ in range(num_samples)]
    num_rock = 0
    num_paper = 0
    num_scissors = 0
    for c in choices:
        if c is rps.Choice.ROCK:
            num_rock += 1
        if c is rps.Choice.PAPER:
            num_paper += 1
        if c is rps.Choice.SCISSORS:
            num_scissors += 1
    #print(f"num_rock = {num_rock}")
    #print(f"num_paper = {num_paper}")
    #print(f"num_scissors = {num_scissors}")
    #print(f"num_rock / num_samples = {num_rock / num_samples}")
    #print(f"strat for rock = {strat[0]}")
    #print(f"num_paper / num_samples = {num_paper / num_samples}")
    #print(f"strat for paper = {strat[1]}")
    #print(f"num_scissors / num_samples = {num_scissors / num_samples}")
    #print(f"strat for scissors = {strat[2]}")
    tolerance = 0.05
    assert abs(num_rock / num_samples - strat[0]) < tolerance
    assert abs(num_paper / num_samples - strat[1]) < tolerance
    assert abs(num_scissors / num_samples - strat[2]) < tolerance


def test_sample_outcome():
    pass

def test_compute_p1_optimal_utility():
    num_samples = 100
    p1_strat = (0.33,0.33,0.34)
    p2_strat = (0.33,0.27,0.40)
    for _ in range(num_samples):
        outcome = rps.sample_outcome(p1_strat, p2_strat)
        assert rps.compute_p1_optimal_utility(outcome) == 1

def test_compute_p1_regret():
    cases = [
        ((rps.Choice.ROCK, rps.Choice.PAPER), (0, 1, 2)),
        ((rps.Choice.PAPER, rps.Choice.PAPER), (0, 0, 1)),
        ((rps.Choice.SCISSORS, rps.Choice.SCISSORS), (1, 0, 0)),
    ]
    for outcome, v in cases:
        r = tuple(rps.compute_p1_regret(outcome))
        print(f"got {r}")
        print(f"expected {v})")
        assert r == v

def test_zero_sum():
    num_samples = 100
    p1_strat = (0.33,0.33,0.34)
    p2_strat = (0.33,0.27,0.40)
    for _ in range(num_samples):
        outcome = rps.sample_outcome(p1_strat, p2_strat)
        u1, u2 = rps.utility(outcome)
        assert u1 + u2 == 0


test_sample_choice()
test_zero_sum()
test_compute_p1_optimal_utility()
test_compute_p1_regret()
