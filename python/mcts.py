
from abc import ABC, abstractmethod, abstractproperty

import logging
logging.basicConfig(filename='/dev/null', level=logging.DEBUG)


class GameState(ABC):

    @abstractmethod
    def next_states(self): pass

    @abstractmethod
    def get_random_next_state(self): pass

    @abstractproperty
    def utility(self): pass

    @abstractproperty
    def is_terminal(self): pass


class Node(ABC):

    def __init__(self, content=None, parent=None):
        if parent:
            assert isinstance(parent, Node)
        self._content = content
        self._parent = parent
        self._children = []

    @property
    def content(self):
        return self._content

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        for c in self.children:
            yield c


class MCTSNode(Node):

    def __init__(self, state, parent=None):
        assert isinstance(state, GameState)
        assert isinstance(parent, MCTSNode)
        super().__init__(
            content=state,
            parent=parent
        )
        self._total_utility = 0
        self._visits = 0
        self._is_expanded = False

    @property
    def state(self):
        return self.content

    @property
    def is_expanded(self):
        return self._is_expanded

    @property
    def children(self):
        if not self.is_expanded:
            self.expand()
        return self.children

    def _expand(self):
        assert not self.is_expanded
        for state in self.state.next_states():
            self._children.append(Node(state, parent=self))
        self._is_expanded = True

    def _backpropogate(self, utility):
        if self.parent is not None:
            self.parent._backpropogate(utility)
        self.total_utility += utility
        self.visits += 1

    def _run_simulation(self):
        s = self.state
        while not s.is_terminal:
            s = s.get_random_next_state()
        return s

    def backpropogate(self):
        self._backpropogate(self.state.utility)


def _UCB1(node):
    from math import sqrt, log, inf
    if node.visits == 0:
        return inf
    exploit = node.total_utility / node.visits
    explore = 2 * sqrt(log(node.parent.visits)/node.visits)
    return exploit + explore


class MCTSTree:

    def __init__(self, root):
        assert isinstance(root, MCTSNode)
        self._root = root
        self._nodes = []

    @property
    def nodes(self):
        for n in self._nodes:
            yield n

    @classmethod
    def from_state(cls, state):
        root = MCTSNode(state)
        return cls(root)


def mcts(state, max_simulations):
    tree = MCTSTree.from_state(state)
    num_expanded = 0
    while num_expanded < max_simulations:
        current = max(tree.nodes, _UCB1)
        while current.is_expanded:
            current = max(current.children, _UCB1)
        if current.num_visits == 0:
            current.backpropogate()
            continue
        tree.add_nodes(current.children)
        num_expanded += 1
