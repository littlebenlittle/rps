
from mcts import GameState

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


