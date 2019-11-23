
import numpy as np
from itertools import product
from collections import namedtuple
from heapq import heappush, heappop
from random import choices as random_choice
from game import Game, Player, Strategy, Outcome, Choice

class TTTMove():
    def __init__(self, x, y):
        if not x in (0,1,2):
            raise ValueError()
        if not y in (0,1,2):
            raise ValueError()
        self.x = x
        self.y = y

class TTTOutcome(Outcome):
    pass

class TTT(Game):

    def __init__(self):
        self.winner = None
        self.state = np.array(
            [[0,0,0],
             [0,0,0],
             [0,0,0]]
        )
        self.win_filters = [
            np.array(
                [[1,1,1],
                 [0,0,0],
                 [0,0,0]]
            ),
            np.array(
                [[0,0,0],
                 [1,1,1],
                 [0,0,0]]
            ),
            np.array(
                [[0,0,0],
                 [0,0,0],
                 [1,1,1]]
            ),
            np.array(
                [[1,0,0],
                 [1,0,0],
                 [1,0,0]]
            ),
            np.array(
                [[0,1,0],
                 [0,1,0],
                 [0,1,0]]
            ),
            np.array(
                [[0,0,1],
                 [0,0,1],
                 [0,0,1]]
            ),
            np.array(
                [[1,0,0],
                 [0,1,0],
                 [0,0,1]]
            ),
            np.array(
                [[0,0,1],
                 [0,1,0],
                 [1,0,0]]
            ),
        ]

    def _send_move(self, x, y, mark):
        if self.state[x,y] != 0:
            raise Exception('Not an empty position!')
        self.state[x,y] = mark

    def send_p1_move(self, move):
        self._send_move(move.x, move.y, 1)

    def send_p2_move(self, move):
        self._send_move(move.x, move.y, 2)

    def is_won(self):
        p1_marked = np.cast[np.int32](self.state == 1)
        p2_marked = np.cast[np.int32](self.state == 2)
        for f in self.win_filters:
            if (p1_marked * f).sum() >= 3:
                self.winner = 1
                return True
            if (p2_marked * f).sum() >= 3:
                self.winner = 2
                return True

class TTTStrategy(Strategy):
    g = TTT()
    def sample(self):
        for _ in range(9):
            p1_choice = self.P1_STRAT.get_choice(g.state)
            g.play(p1_choice)
            if g.won():
                break
            p2_choice = self.P2_STRAT.get_choice(g.state)
            g.play(p2_choice)
            if g.won():
                break
        return TTTOutcome(p1_choices, p2_choices)

class TTTPlayer(Player):
    pass

class RandomPlayer(TTTPlayer):
    def select_move(self, game_state):
        xs, ys = np.where(game_state==0)
        if len(xs) == 0:
            raise Exception('No valid moves')
        selection = random_choice(range(len(xs)))[0]
        return TTTMove(xs[selection], ys[selection])

class TTTState():
    def __init__(self, state):
        self.state = state.copy()
    def __eq__(self, other):
        return (self.state == other.state).all()
    def __lt__(self, other):
        return None
    def __repr__(self):
        return f'<ttt.TTTState \n{self.state.__repr__()}>'
    def next_states(self, num_samples=None):
        if (np.cast[np.int32](self.state != 0).sum() % 2) == 0:
            mark = 1
        else:
            mark = 2
        for x,y in product(range(3),range(3)):
            if self.state[x,y] != 0:
                continue
            k = self.state.copy()
            k[x,y] = mark
            yield TTTState(k)

# TODO: find a library for this 2019-11-22Z14:30:02
_Node = namedtuple('node', ['state','parent'])
class DecisionTree():
    def __init__(self, init_state, max_heap_size):
        self.Q = []
        self.max_heap_size = max_heap_size
        n = _Node(init_state, None)
        heappush(self.Q, (0., n))
    def expand_next_node(self, priority_fn):
        p, node = heappop(self.Q)
        for next_state in node.state.next_states():
            p = priority_fn(next_state)
            n = _Node(next_state, node)
            heappush(self.Q, (p, n))

class RegretMatchingPlayer(TTTPlayer):
    def select_move(self, game_state):
        for _ in range(1000):
            s1 = self.p1_strategy.sample()
            s2 = self.p2_strategy.sample()

    def priority(self, state):
        pass

    def ponder(self, states, Q=None):
        if not Q:
            Q = StateQueue()
        for state in game.get_next_states(state):
            Q.push(state, self.priority(state))
        for _ in range(1000):
            priorities = [p for p, _ in Q]
            states = [s for _, s in Q]
            weights = self.compute_weights(priorities)
            state = get_random_choice(states, weights)
            for nxt_state in game.get_next_states(state):
                p = self.priority(state)
                heappush(Q, (p, state))
