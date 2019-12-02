
import numpy as np
from games import NimState, TTTState
from ttt import BEGIN

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


def test_TTTState():
    assert TTTState.from_array(BEGIN) \
           == TTTState(np.zeros([3,3]), np.zeros([3,3]))
    s = TTTState.from_array(np.array(
        [[1,0,2],
         [0,0,1],
         [1,0,2]]
    ))
    assert not s.is_terminal
    return
    for _ in range(100):
        s = TTTState(BEGIN)
        while not s.is_terminal:
            s_ = s.get_random_next_state()
            assert s_ in list(s.next_states)
