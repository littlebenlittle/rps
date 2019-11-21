
import numpy as np
from random import choices
from game import Game, Player, Strategy, Outcome, Choice

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
        p1_choice = choices(
            list(RPSChoice),
            weights=list(self.P1_STRAT)
        )[0]
        p2_choice = choices(
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
        u_opt = max([self.utility(o) for o in outcomes])
        return u_opt - u

    def utility(self, outcome):
        p1_choice = outcome.P1_CHOICE
        p2_choice = outcome.P2_CHOICE
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
        

def main():
    pass


if __name__ == '__main__':
    main()
