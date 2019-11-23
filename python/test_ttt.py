
import logging
import numpy as np
from ttt import *

logging.basicConfig(filename='/dev/null', level=logging.DEBUG)

START = np.array(
    [[0,0,0],
     [0,0,0],
     [0,0,0],]
)

def test_ttt():
    game = TTT()
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    mv = p1.select_move(game.state)
    game.send_p1_move(mv)
    mv = p2.select_move(game.state)
    game.send_p2_move(mv)
    assert not game.is_won()

def test_TTTState():
    s = TTTState(START)
    valid_1st_moves = []
    for i in range(9):
        x = i % 3
        y = i // 3
        A = START.copy()
        A[x,y] = 1
        valid_1st_moves.append(TTTState(A))
    for ns in s.next_states():
        assert ns in valid_1st_moves
    for mv in valid_1st_moves:
        assert mv in s.next_states()

def test_DecisionTree():
    A = START.copy()
    A[0,0] = 1
    A[1,1] = 2
    A[0,1] = 1
    A[0,2] = 2
    dt = DecisionTree(
        init_state=TTTState(A),
        max_heap_size=None,
    )
    dt.expand_next_node(lambda _: 1)
    states = [n.state for _,n in dt.Q]
    for s in states:
        print(s)
    assert False

def test_TTT_is_won():
    g = TTT()
    assert not g.is_won()
    assert g.winner == None
    g.send_p1_move(TTTMove(0,0))
    g.send_p1_move(TTTMove(1,1))
    g.send_p1_move(TTTMove(2,2))
    assert g.is_won()
    assert g.winner == 1
    g = TTT()
    g.send_p2_move(TTTMove(0,0))
    g.send_p2_move(TTTMove(1,0))
    g.send_p2_move(TTTMove(2,0))
    assert g.is_won()
    assert g.winner == 2
    g = TTT()
    g.send_p1_move(TTTMove(0,0))
    g.send_p2_move(TTTMove(1,1))
    g.send_p1_move(TTTMove(2,2))
    assert not g.is_won()
    assert g.winner == None

def test_TTTStrategy_sample():
    pass

def test_TTTPlayer_utility():
    pass

def test_TTTPlayer_regret():
    pass

def test_RegretMatchingPlayer_update_strategy():
    pass

def test_RegretMatchingPlayer():
    pass
