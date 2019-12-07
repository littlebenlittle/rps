
from games import NimState, TTTState
from mcts import mcts, MCTSTree, MCTSNode
from ttt import BEGIN

import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.setLevel(logging.INFO)

def test_mcts():
    nim_state = NimState(25, 1)
    tree = mcts(
        state=nim_state,
        max_simulations=100,
        utility_fn=lambda s: 1 if s.num_beads <= 3 and s.player_turn == 1 else 0,
    )
    state = TTTState.from_array(BEGIN)
    tree = mcts(
        state=state,
        max_simulations=1000,
        utility_fn=(lambda s:
            1  if s.winner == 'X' else
            -1 if s.winner == 'O'
            else 0
        )
    )
    for n in sorted(tree.nodes, key=lambda n: n.visits):
        logger.info(f'{n.state} {n.visits}')
    assert False

def test_MCTSNode():
    nim_state = NimState(25, 1)
    nim_state_other = NimState(20, 1)
    node = MCTSNode(nim_state)
    assert node.state == nim_state
    assert node.state != nim_state_other
    assert len(set(node.children)) == 0
    node.expand()
    assert len(set(node.children)) != 0
    try:
        node.expand()
        assert False
    except Exception:
        pass
    a = MCTSNode.singleton(NimState(25, 1))
    b = MCTSNode.singleton(NimState(25, 1))
    print(hash(a))
    print(hash(b))
    assert a is b
    b = MCTSNode.singleton(NimState(24, 1))
    print(hash(b))
    assert not a is b


def test_MCTSTree():
    nim_state = NimState(25, 1)
    nim_tree = MCTSTree.from_state(nim_state)
    nim_tree_states = [n.state for n in nim_tree.nodes]
    ttt_state = TTTState.from_array(BEGIN)
    ttt_tree = MCTSTree.from_state(ttt_state)
    ttt_tree_states = [n.state for n in ttt_tree.nodes]
    assert nim_state in nim_tree_states
    assert ttt_state in ttt_tree_states
    assert not ttt_state in [n.state for n in nim_tree.nodes]
    assert not nim_state in [n.state for n in ttt_tree.nodes]
    root_node = MCTSNode(nim_state)
    tree = MCTSTree(root_node)
    root_node.expand()
    tree.add_nodes(root_node.children)
    for s in nim_state.next_states:
        assert s in [n.state for n in tree.nodes]
