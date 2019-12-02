
from abc import ABC, abstractmethod, abstractproperty

# TODO: centralize logging 2019-12-01Z15:30:32
import logging
logging.basicConfig(filename='/dev/null', level=logging.DEBUG)


class GameState(ABC):

    @abstractproperty
    def is_terminal(self): pass

    @abstractproperty
    def next_states(self): pass

    @abstractmethod
    def get_random_next_state(self): pass


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
        for c in self._children:
            yield c


class MCTSNode(Node):

    def __init__(self, state, parent=None):
        assert isinstance(state, GameState)
        if parent:
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
    def visits(self):
        return self._visits

    @property
    def total_utility(self):
        return self._total_utility

    @property
    def is_expanded(self):
        return self._is_expanded

    def expand(self):
        if not self.is_expanded:
            assert not self.is_expanded
            for state in self.state.next_states:
                self._children.append(MCTSNode(state, parent=self))
            self._is_expanded = True

    def run_simulation(self):
        s = self.state
        while not s.is_terminal:
            s = s.get_random_next_state()
        return s

    def backpropogate(self, utility):
        if self.parent is not None:
            self.parent.backpropogate(utility)
        self._total_utility += utility
        self._visits += 1


class MCTSTree:

    def __init__(self, root):
        assert isinstance(root, MCTSNode)
        self._root = root
        self._nodes = [root]

    def __repr__(self):
        s = '\n'.join(['    ' + n.__repr__() for n in self.nodes])
        return f"<MCTSTree\nnodes:\n{s}\n>"

    @property
    def nodes(self):
        for n in self._nodes:
            yield n

    def add_nodes(self, nodes):
        for n in nodes:
            assert isinstance(n, MCTSNode)
        self._nodes.extend(nodes)

    @classmethod
    def from_state(cls, state):
        root = MCTSNode(state)
        return cls(root)


def _UCB1(node):
    from math import sqrt, log, inf
    if node.visits == 0 or node.parent is None:
        return inf
    exploit = node.total_utility / node.visits
    explore = 2 * sqrt(log(node.parent.visits)/node.visits)
    return exploit + explore


def mcts(state, max_simulations, utility_fn):
    tree = MCTSTree.from_state(state)
    num_expanded = 0
    while num_expanded < max_simulations:
        current = max(tree.nodes, key=_UCB1)
        while current.is_expanded:
            current = max(current.children, key=_UCB1)
        if current.visits == 0:
            s = current.run_simulation()
            utility = utility_fn(s)
            current.backpropogate(utility)
            continue
        current.expand()
        tree.add_nodes(current.children)
        num_expanded += 1
    return tree
