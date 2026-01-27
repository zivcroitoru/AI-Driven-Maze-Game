import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core_types import Action

def test_action_delta():
    assert Action.delta(Action.UP) == (-1, 0)
    assert Action.delta(Action.DOWN) == (1, 0)
    assert Action.delta(Action.LEFT) == (0, -1)
    assert Action.delta(Action.RIGHT) == (0, 1)

def test_action_delta_invalid():
    import pytest
    with pytest.raises(ValueError):
        Action.delta(999)
