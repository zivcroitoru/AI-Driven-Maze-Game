import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.environment import Environment
from src.core_types import Action
import numpy as np
def test_reset_returns_start_position():
    grid = np.zeros((5, 5), dtype=int)
    start = (0, 0)
    goal = (4, 4)
    env = Environment(grid, start, goal)
    state = env.reset()
    assert state == start

def test_valid_move_updates_position_and_returns_step_penalty():
    grid = np.zeros((5, 5), dtype=int)
    start = (2, 2)
    goal = (4, 4)
    env = Environment(grid, start, goal)
    env.reset()
    next_state, reward, done = env.step(Action.DOWN)  # move down
    assert next_state == (3, 2)
    assert reward == -1.0
    assert done is False

def test_invalid_move_into_wall_returns_penalty():
    grid = np.zeros((5, 5), dtype=int)
    grid[2][3] = 1  # set a wall to the right
    env = Environment(grid, (2, 2), (4, 4))
    env.reset()
    next_state, reward, done = env.step(Action.RIGHT)  # move into wall
    assert next_state == (2, 2)  # no movement
    assert reward == -10.0
    assert done is False

def test_goal_reached_gives_positive_reward_and_ends_episode():
    grid = np.zeros((5, 5), dtype=int)
    env = Environment(grid, (0, 0), (0, 1))
    env.reset()
    next_state, reward, done = env.step(Action.RIGHT)  # move into goal
    assert next_state == (0, 1)
    assert reward == 100.0
    assert done is True

def test_episode_ends_after_max_steps():
    grid = np.zeros((5, 5), dtype=int)
    env = Environment(grid, (0, 0), (4, 4), maxSteps=2)
    env.reset()
    env.step(Action.DOWN)
    next_state, reward, done = env.step(Action.DOWN)  # should hit max steps
    assert done is True
