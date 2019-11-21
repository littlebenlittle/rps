
import numpy as np
from random import choices as random_choice
from game import Player, Strategy, Outcome, Choice

class RPSOutcome(Outcome):
    def __init__(self, p1_choice, p2_choice):
        self.P1_CHOICE = p1_choice
        self.P2_CHOICE = p2_choice

    def __eq__(self, other):
        return  self.P1_CHOICE == other.P1_CHOICE \
            and self.P2_CHOICE == other.P2_CHOICE

class RPSChoice(Choice):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class RPSStrategy(Strategy):
    def sample(self):
        p1_choice = random_choice(
            list(RPSChoice),
            weights=list(self.P1_STRAT)
        )[0]
        p2_choice = random_choice(
            list(RPSChoice),
            weights=list(self.P2_STRAT)
        )[0]
        return RPSOutcome(p1_choice, p2_choice)

class RPSPlayer(Player):

    def __init__(self):
        self.choices = RPSChoice
 
    def regret(self, outcome):
        p1_choice = outcome.P1_CHOICE
        p2_choice = outcome.P2_CHOICE
        u = self.utility(outcome)
        outcomes = [RPSOutcome(c, p2_choice) for c in self.choices]
        u_ = self.utility(outcomes)
        return np.maximum(u_ - u, 0)

    def utility(self, outcomes):
        try:
            u = []
            for o in outcomes:
                u.append(self._utility(o))
            return np.array(u)
        except TypeError:
            return np.array([self._utility(outcomes)])

    def _utility(self, outcome):
        # TODO: clean this up 2019-11-20Z17:22:28
        if outcome == RPSOutcome(RPSChoice.ROCK, RPSChoice.ROCK):
            return 0
        if outcome == RPSOutcome(RPSChoice.ROCK, RPSChoice.PAPER):
            return -1
        if outcome == RPSOutcome(RPSChoice.ROCK, RPSChoice.SCISSORS):
            return 1
        if outcome == RPSOutcome(RPSChoice.PAPER, RPSChoice.ROCK):
            return 1
        if outcome == RPSOutcome(RPSChoice.PAPER, RPSChoice.PAPER):
            return 0
        if outcome == RPSOutcome(RPSChoice.PAPER, RPSChoice.SCISSORS):
            return -1
        if outcome == RPSOutcome(RPSChoice.SCISSORS, RPSChoice.ROCK):
            return -1
        if outcome == RPSOutcome(RPSChoice.SCISSORS, RPSChoice.PAPER):
            return 1
        if outcome == RPSOutcome(RPSChoice.SCISSORS, RPSChoice.SCISSORS):
            return 0


    def strategy_for(self, choice):
        if choice is RPSChoice.ROCK:
            return self.strategy[0]
        if choice is RPSChoice.PAPER:
            return self.strategy[1]
        if choice is RPSChoice.SCISSORS:
            return self.strategy[2]
        
class ConstantPlayer(RPSPlayer):
    def __init__(self, strategy):
        self.strategy = strategy

class RegretMatchingPlayer(RPSPlayer):

    def __init__(self, blind_strategy=(np.array([1.,1.,1.]) / 3.)):
        super().__init__()
        self.strategy = blind_strategy
        self.cumulative_regret = np.array([0, 0, 0])

    def update_strategy(self, outcome):
        self.cumulative_regret += self.regret(outcome)
        total_regret = self.cumulative_regret.sum()
        if total_regret == 0:
            self.strategy = np.array([1.,1.,1.]) / 3.
            return
        self.strategy = self.cumulative_regret / total_regret
