import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pathfinder import Pathfinder
from core_types import Action
import numpy as np

def test_astar_finds_path():
    grid = np.zeros((5, 5), dtype=int)
    start = (0, 0)
    goal = (2, 2)

    pf = Pathfinder()
    path = pf.getAStarPath(grid, start, goal)

    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
    assert len(path) >= 3  # at least a few steps

def test_astar_returns_none_if_no_path():
    grid = np.ones((5, 5), dtype=int)
    grid[0][0] = 0  # start
    grid[4][4] = 0  # goal

    pf = Pathfinder()
    path = pf.getAStarPath(grid, (0, 0), (4, 4))
    assert path is None

def test_astar_start_equals_goal():
    grid = np.zeros((3, 3), dtype=int)
    pf = Pathfinder()
    path = pf.getAStarPath(grid, (1, 1), (1, 1))
    assert path == [(1, 1)]

def test_next_move_from_path():
    path = [(1, 1), (1, 2)]
    pf = Pathfinder()
    action = pf.nextMoveFromPath(path)
    assert action == Action.RIGHT

def test_next_move_returns_none_on_short_path():
    pf = Pathfinder()
    assert pf.nextMoveFromPath(None) is None
    assert pf.nextMoveFromPath([]) is None
    assert pf.nextMoveFromPath([(1, 1)]) is None
