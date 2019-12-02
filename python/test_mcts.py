
import numpy as np
# TODO: no wildcard imports 2019-12-01Z15:43:44
from mcts import *


class NimState(GameState):

    def __init__(self, num_beads, num_takeaway=3):
        self._num_beads = num_beads
        self._num_takeaway = num_takeaway

    def __repr__(self):
        return f'<NimState: {self._num_beads}>'

    def __eq__(self, other):
        return self._num_beads == other._num_beads \
                and self._num_takeaway == other._num_takeaway

    @property
    def num_takeaway(self):
        return self._num_takeaway

    @property
    def num_beads(self):
        return self._num_beads

    @property
    def is_terminal(self):
        return self.num_beads <= self.num_takeaway

    @property
    def next_states(self):
        for n in range(1, self._num_takeaway+1):
            yield NimState(
                self.num_beads - n,
                self.num_takeaway,
            )

    def get_random_next_state(self):
        from random import choice
        n = choice(range(1, self.num_takeaway+1))
        return NimState(
            self.num_beads - n,
            self.num_takeaway,
        )


def test_NimState():
    assert NimState(25, num_takeaway=5) == NimState(25, num_takeaway=5) 
    assert NimState(25, num_takeaway=3) == NimState(25) 
    assert NimState(25, num_takeaway=3) != NimState(24) 
    assert NimState(2).is_terminal
    assert not NimState(3, num_takeaway=2).is_terminal
    s = NimState(25)
    for s_ in s.next_states:
        assert s.num_takeaway == s_.num_takeaway
    for _ in range(100):
        s_ = s.get_random_next_state()
        assert s_ in list(s.next_states)
