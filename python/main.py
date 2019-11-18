
from random import choices
from rps import Game, Player, Strategy, Outcome, Choice

# TODO: use enum? 2019-11-18Z11:39:39
WIN = "win"
LOSE = "loss"
TIE = "tie"

def get_outcome(p1_choice, p2_choice):
    if p1_choice == RPSChoice.ROCK:
        if p2_choice == RPSChoice.ROCK:
            return RPSOutcome.TIE
        elif p2_choice == RPSChoice.PAPER:
            return RPSOutcome.LOSE
        else:
            return RPSOutcome.WIN
    elif p1_choice == RPSChoice.PAPER:
        if p2_choice == RPSChoice.ROCK:
            return RPSOutcome.WIN
        elif p2_choice == RPSChoice.PAPER:
            return RPSOutcome.TIE
        else:
            return RPSOutcome.LOSE
    elif p1_choice == RPSChoice.SCISSORS:
        if p2_choice == RPSChoice.ROCK:
            return RPSOutcome.LOSE
        elif p2_choice == RPSChoice.PAPER:
            return RPSOutcome.WIN
        else:
            return RPSOutcome.TIE
    else:
        raise ValueError('Choice must be one of RPSChoice.ROCK, RPSChoice.PAPER, RPSChoice.SCISSORS')

class RPS(Game):
    def choose(self, choice):
        CHOICES = list(RPSChoice)
        P2_STRAT = (0.4, 0.3, 0.3)
        p2_choice = choices(self.CHOICES, weights=list(P2_STRAT))[0]
        return get_outcome(choice, p2_choice)

class RPSStrategy(Strategy):
    def sample(self):
        p1_choice = choices(
            [RPSChoice.ROCK, RPSChoice.PAPER, RPSChoice.SCISSORS],
            weights=list(P1_STRAT)
        )[0]
        p2_choice = choices(
            [RPSChoice.ROCK, RPSChoice.PAPER, RPSChoice.SCISSORS],
            weights=list(P2_STRAT)
        )[0]
        return get_outcome(p1_choice, p2_choice)

class RPSOutcome(Outcome):
    WIN = 1
    TIE = 2
    LOSE = 3

class RPSChoice(Choice):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RPSPlayer(Player):
    def regret(self, choice, outcome):
        if choice == RPSChoice.ROCK:
            if outcome == RPSOutcome.WIN:
                return (0, 0, 0)
            if outcome == RPSOutcome.TIE:
                return (0, 1, 0)
            if outcome == RPSOutcome.LOSE:
                return (0, 1, 2)
        if choice == RPSChoice.PAPER:
            if outcome == RPSOutcome.WIN:
                return (0, 0, 0)
            if outcome == RPSOutcome.TIE:
                return (0, 0, 1)
            if outcome == RPSOutcome.LOSE:
                return (2, 0, 1)
        if choice == RPSChoice.SCISSORS:
            if outcome == RPSOutcome.WIN:
                return (0, 0, 0)
            if outcome == RPSOutcome.TIE:
                return (1, 0, 0)
            if outcome == RPSOutcome.LOSE:
                return (1, 2, 0)
        raise ValueError(f'choice must be one of "win", "tie", "loss"; got {choice}')

    def _regret(self, outcome):
        for choice in list(RPSChoice):
            u_opt = 1

    def utility(self, outcome):
        if outcome == WIN:
            return 1
        if outcome == LOSE:
            return -1
        if outcome == TIE:
            return 0


def main():
    pass


if __name__ == '__main__':
    main()
