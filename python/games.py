
import numpy as np
from mcts import GameState
from ttt import BEGIN, WIN_FILTERS

import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.setLevel(logging.WARN)


class NimState(GameState):

    def __init__(self, num_beads, player_turn, num_takeaway=3):
        self._num_beads = num_beads
        assert player_turn in (1,2)
        self._player_turn = player_turn
        self._num_takeaway = num_takeaway

    def __repr__(self):
        return f'<NimState: {self._num_beads}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other) 

    def __hash__(self):
        return hash((self.num_beads, self.num_takeaway))

    @property
    def num_takeaway(self):
        return self._num_takeaway

    @property
    def player_turn(self):
        return self._player_turn

    @property
    def num_beads(self):
        return self._num_beads

    @property
    def is_terminal(self):
        return self.num_beads <= self.num_takeaway

    @property
    def next_states(self):
        if self.is_terminal:
            return None
        if self.player_turn == 2:
            for n in range(1, self._num_takeaway+1):
                s = NimState(
                    max(self.num_beads - n, 0),
                    1,
                    self.num_takeaway,
                )
                yield s
        else:
            for n in range(1, self._num_takeaway+1):
                next_state = NimState(
                    max(self.num_beads - n, 0),
                    2,
                    self.num_takeaway,
                )
                for s in next_state.next_states:
                    if s is not None:
                        yield s

    def get_random_next_state(self):
        from random import choice
        n = choice(range(1, self.num_takeaway+1))
        return NimState(
            self.num_beads - n,
            1 if self.player_turn == 2 else 2,
            self.num_takeaway,
        )


class TTTState(GameState):

    def __init__(self, x_locations, o_locations):
        self._x_loc = x_locations.astype(np.int32)
        self._o_loc = o_locations.astype(np.int32)
        self._winner = None

    def __repr__(self):
        # TODO: pretty print Xs and Os 2019-12-02Z12:54:24
        image = self.x_loc.copy()
        image += self.o_loc * 2
        return f"\n<TTTState {image[0]}\n" \
            + " " * 10 + f"{image[1]}\n" \
            + " " * 10 + f"{image[2]}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other) 

    def __hash__(self):
        return hash((self.x_loc.dumps(), self.o_loc.dumps()))


    @property
    def x_loc(self):
        return self._x_loc

    @property
    def o_loc(self):
        return self._o_loc

    @property
    def is_terminal(self):
        if self.winner:
            return True
        # TODO: this is hard to interpret 2019-12-02Z15:34:03
        num_marks = (self.x_loc + self.o_loc).astype(np.bool).astype(np.int).sum()
        return num_marks == 9

    @property
    def next_states(self):
        from itertools import product
        num_xs = (np.ones([3,3]) * self.x_loc).sum()
        num_os = (np.ones([3,3]) * self.o_loc).sum()
        x_locations = self.x_loc.copy()
        o_locations = self.o_loc.copy()
        is_x_turn = (num_xs == num_os)
        if is_x_turn:
            for i, j in product(range(3),range(3)):
                if not (self.x_loc[i,j] or self.o_loc[i,j]):
                    x_locations[i,j] = 1
                    yield TTTState(x_locations, o_locations)
        else:
            for i, j in product(range(3),range(3)):
                if not (self.x_loc[i,j] or self.o_loc[i,j]):
                    o_locations[i,j] = 1
                    next_state = TTTState(x_locations, o_locations)
                    for s in next_state.next_states:
                        yield s

    def get_random_next_state(self):
        # TODO: this is not efficient 2019-12-02Z13:03:16
        from random import choice
        return choice(list(self.next_states))

    @classmethod
    def from_array(cls, array):
        xs = (array == 1).astype(np.int)
        os = (array == 2).astype(np.int)
        return cls(xs, os)

    @property
    def winner(self):
        # TODO: implement "@cachedproperty" maybe ? 2019-12-02Z12:05:41
        # does opcache make this ^ irrelevant?
        if not self._winner:
            for wf in WIN_FILTERS:
                # compute the dot product (as a 9-dim inner product space)
                if (self.x_loc * wf).sum() == 3:
                    self._winner = 'X'
                if (self.o_loc * wf).sum() == 3:
                    self._winner = 'O'
        return self._winner
