
from random import choices
from enum import Enum
from functools import reduce


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def sample_choice(strat):
    return choices(
        [Choice.ROCK, Choice.PAPER, Choice.SCISSORS],
        weights=list(strat),
    )[0]


def sample_outcome(p1_strat, p2_strat):
    p1_choice = sample_choice(p1_strat)
    p2_choice = sample_choice(p2_strat)
    return p1_choice, p2_choice


def utility(outcome):
    p1_choice, p2_choice = outcome
    if p1_choice is Choice.ROCK:
        if p2_choice is Choice.ROCK:
            return (0,0)
        if p2_choice is Choice.PAPER:
            return (-1,1)
        if p2_choice is Choice.SCISSORS:
            return (1,-1)
    if p1_choice is Choice.PAPER:
        if p2_choice is Choice.ROCK:
            return (1,-1)
        if p2_choice is Choice.PAPER:
            return (0,0)
        if p2_choice is Choice.SCISSORS:
            return (-1,1)
    if p1_choice is Choice.SCISSORS:
        if p2_choice is Choice.ROCK:
            return (-1,1)
        if p2_choice is Choice.PAPER:
            return (1,-1)
        if p2_choice is Choice.SCISSORS:
            return (0,0)


def compute_p1_optimal_utility(outcome):
    # O(num_p1_choices)
    _, c2 = outcome
    p1_choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
    u_opt = -10
    for c in p1_choices:
        outcome = c, c2
        u, _ = utility(outcome)
        if u > u_opt:
            u_opt = u
    return u_opt

def compute_p1_regret(outcome):
    u, _ = utility(outcome)
    _, p2_choice = outcome
    p1_choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
    for c in p1_choices:
        proposed_outcome = c, p2_choice
        u_, _ = utility(proposed_outcome)
        yield max(0, u_ - u)

def compute_p1_cumulative_regret(hist):
    p1_choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
    cum_regret = {}
    for c in p1_choices:
        cum_regret[c.name] = 0
    for outcome in hist:
        regret = tuple(compute_p1_regret(outcome))
        cum_regret["ROCK"] += regret[0]
        cum_regret["PAPER"] += regret[1]
        cum_regret["SCISSORS"] += regret[2]
        # print(f"cum_regret[{p1_choice.name}] = {cum_regret[p1_choice.name]}")
    return (
        cum_regret["ROCK"],
        cum_regret["PAPER"],
        cum_regret["SCISSORS"],
    )


def compute_p1_strat(p1_strat, hist):
    regret = compute_p1_cumulative_regret(hist)
    print(regret)
    total_regret = reduce(lambda a,b: a+b, regret, 0)
    if total_regret == 0:
        return (0.33, 0.33, 0.34)
    return (
        regret[0] / total_regret,
        regret[1] / total_regret,
        regret[2] / total_regret,
    )


def compute_p2_strat(p2_strat, hist):
    # for outcome in hist:
        # _, u = utility(outcome)
    return p2_strat


def get_blind_p1_strat():
    return (0.25, 0.15, 0.6)


def get_blind_p2_strat():
    return (0.4, 0.3, 0.3)


def main():
    # players 1 and 2 select a blind strategy
    # for some number of rounds:
    #   An outcome is sampled based on p1 and p2 strategy
    #   Players select a new strategy
    p1_strat = get_blind_p1_strat()
    p2_strat = get_blind_p2_strat()
    num_rounds = 5000
    hist = []
    for i in range(num_rounds):
        print(f"strats = {p1_strat}, {p2_strat}")
        outcome = sample_outcome(p1_strat, p2_strat)
        hist.append(outcome)
        print(f"outcome = {[x.name for x in outcome]}")
        p1_strat = compute_p1_strat(p1_strat, hist)
        p2_strat = compute_p2_strat(p2_strat, hist)


if __name__ == '__main__':
     main()
