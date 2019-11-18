
from random import choices
from game import Game, Player, Strategy, Outcome, Choice

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
            weights=list(self.P1_STRAT)
        )[0]
        p2_choice = choices(
            [RPSChoice.ROCK, RPSChoice.PAPER, RPSChoice.SCISSORS],
            weights=list(self.P2_STRAT)
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

    def _regret(self, strategy):
        u_opt = 1
        for choice in list(RPSChoice):
            u = self.utility()

    def utility(self, strategy):
        u = 0
        n = 1000
        for _ in range(n):
            outcome = strategy.sample()
            if outcome == RPSOutcome.WIN:
                u += 1
            elif outcome == RPSOutcome.LOSE:
                u -= 1
        return u/n


def main():
    pass


if __name__ == '__main__':
    main()
