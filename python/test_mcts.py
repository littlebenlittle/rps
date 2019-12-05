
from games import NimState, TTTState
from mcts import mcts
from ttt import BEGIN


def test_mcts():
    s = NimState(25)
    def p1_utility(s):
        if s.num_beads <= 3:
            return 1
    tree = mcts(s, 5, lambda s: 1 if s.num_beads <= 3 else 0)
    print(tree)
    s = TTTState.from_array(BEGIN)
    tree = mcts(s, 5, lambda s: 1 if s.winner == 'X' else (-1 if s.winner == 'O' else 0))
    print(tree)
    assert False
