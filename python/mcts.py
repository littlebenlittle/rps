
from abc import ABC, abstractmethod, abstractproperty

import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.setLevel(logging.WARN)

class GameState(ABC):

    @abstractproperty
    def is_terminal(self): pass

    @abstractproperty
    def next_states(self): pass

    @abstractmethod
    def get_random_next_state(self): pass

    # TODO: use abc 2019-12-06Z21:02:27
    @abstractmethod
    def __hash__(self): pass


class Node(ABC):

    # TODO: metaclass with factory for __init__ 2019-12-06Z20:06:40
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

    def add_child(self, child):
        assert self.content.__class__ == child.content.__class__
        self._children.append(child)


_MCTSNode_singletons = {}

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

    # TODO: check the privacy requirements of this 2019-12-07Z12:04:27
    @classmethod
    def singleton(cls, state, parent=None):
        h = hash(state)
        if h in _MCTSNode_singletons.keys():
            return _MCTSNode_singletons[h]
        new_node = cls(state, parent)
        _MCTSNode_singletons[h] = new_node
        return new_node

    def expand(self):
        assert not self.is_expanded
        for state in self.state.next_states:
            self.add_child(MCTSNode.singleton(state, parent=self))
        self._is_expanded = True

    def run_simulation(self):
        # TODO: this does not seem to be working 2019-12-06Z21:24:57
        s = self.state
        while not s.is_terminal:
            s = s.get_random_next_state()
            logger.debug(f'selected {s}')
        return s

    def backpropogate(self, utility):
        if self.parent is not None:
            self.parent.backpropogate(utility)
        self._total_utility += utility
        self._visits += 1


# TODO: incorporate a tree library 2019-12-07Z11:57:39
class MCTSTree:

    def __init__(self, root):
        assert isinstance(root, MCTSNode)
        self._root = root
        self._nodes = set([root])

    @property
    def root(self):
        return self._root

    @property
    def nodes(self):
        for n in self._nodes:
            yield n

    def add_nodes(self, nodes):
        for n in nodes:
            assert isinstance(n, MCTSNode)
            self._nodes.add(n)

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


def get_next_node(tree):
    current = tree.root
    logger.info(f'selected {current.state} with UCB1 of {_UCB1(current)}')
    while current.is_expanded:
        if current.state.is_terminal:
            logger.info(f'*** terminal state found ***')
            logger.info(f'state: {current.state}')
            break
        logger.debug(f'node already expanded. selecting from children')
        current = max(current.children, key=_UCB1)
        logger.debug(f'selected {current.state} with UCB1 of {_UCB1(current)}')
    logger.info(f'selected {current.state} with UCB1 of {_UCB1(current)}')
    return current


def mcts(state, max_simulations, utility_fn, verbose=False): 
    tree = MCTSTree.from_state(state)
    num_simulations = 0
    while num_simulations < max_simulations:
        logger.info('*** selecting node with highest UCB1 value ***')
        current = get_next_node(tree)
        if current.visits == 0 or current.state.is_terminal:
            if current.state.is_terminal:
                logger.info('*** reached terminal node ***')
            else:
                logger.info('*** node has not been visited. simulating ***')
            s = current.run_simulation()
            num_simulations += 1
            utility = utility_fn(s)
            current.backpropogate(utility)
            logger.info(f'simulated utility: {utility}')
            continue
        logger.info('*** node already visited. expanding ***')
        current.expand()
        logger.info(f'{len(set(current.children))} children found')
        tree.add_nodes(current.children)
    return tree
