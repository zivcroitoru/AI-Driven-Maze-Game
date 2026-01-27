import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from maze_generator import MazeGenerator
from core_types import MazeGenParams
import numpy as np

def test_generate_creates_valid_grid():
    mg = MazeGenerator()
    params = MazeGenParams(rows=5, cols=5, wallDensity=0.2, maxTries=5, seed=42)
    grid, start, goal = mg.generate(params)

    assert isinstance(grid, list)
    assert grid[start[0]][start[1]] == 0
    assert grid[goal[0]][goal[1]] == 0

def test_generate_with_different_seeds():
    mg = MazeGenerator()
    p1 = MazeGenParams(rows=5, cols=5, wallDensity=0.3, maxTries=5, seed=1)
    p2 = MazeGenParams(rows=5, cols=5, wallDensity=0.3, maxTries=5, seed=999)

    g1, _, _ = mg.generate(p1)
    g2, _, _ = mg.generate(p2)

    assert g1 != g2  # different seeds → different mazes (usually)

def test_generate_fallback_to_empty_if_unsolvable():
    mg = MazeGenerator()
    # very high wall density should force it to give up and return empty
    params = MazeGenParams(rows=3, cols=3, wallDensity=0.99, maxTries=1, seed=123)
    grid, _, _ = mg.generate(params)

    all_zero = all(cell == 0 for row in grid for cell in row)
    assert all_zero  # should return empty grid fallback

def test_ensure_solvable_detects_unsolvable():
    mg = MazeGenerator()
    grid = np.ones((3, 3), dtype=int)
    grid[0][0] = 0
    grid[2][2] = 0

    assert not mg.ensureSolvable(grid.tolist(), (0, 0), (2, 2))

def test_ensure_solvable_detects_solvable():
    mg = MazeGenerator()
    grid = np.zeros((3, 3), dtype=int)
    assert mg.ensureSolvable(grid.tolist(), (0, 0), (2, 2))
