import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hybrid_agent import HybridAgent
from src.environment import Environment
from src.core_types import Action

import numpy as np

def create_simple_env():
    grid = np.zeros((5, 5), dtype=int)
    start = (0, 0)
    goal = (4, 4)
    return Environment(grid, start, goal)

def test_q_table_updates_correctly():
    agent = HybridAgent(alpha=0.5, gamma=0.9, epsilon=0.0, heuristicRate=0.0)
    state = (0, 0)
    next_state = (0, 1)
    action = Action.RIGHT
    reward = 10.0

    agent.updateQ(state, action, reward, next_state)
    value = agent.qTable[state][action]
    assert value != 0.0  # Should be updated
    assert 0.0 < value <= reward  # Should be within reasonable range

def test_get_action_returns_valid_action():
    env = create_simple_env()
    agent = HybridAgent(alpha=0.5, gamma=0.9, epsilon=1.0, heuristicRate=0.0)  # use exploration to trigger random
    state = env.reset()

    valid_actions = [a for a in Action.ALL if env.isValidMove(a)]
    if valid_actions:
        action = agent.getAction(state, env)
        assert action in valid_actions

def test_reset_q_table_clears_all_data():
    agent = HybridAgent(alpha=0.5, gamma=0.9, epsilon=0.0, heuristicRate=0.0)
    agent.updateQ((0, 0), Action.RIGHT, 1.0, (0, 1))
    assert len(agent.qTable) > 0

    agent.resetQTable()
    assert len(agent.qTable) == 0

def test_set_epsilon_and_heuristic_rate():
    agent = HybridAgent(alpha=0.5, gamma=0.9, epsilon=0.1, heuristicRate=0.2)
    agent.setEpsilon(0.9)
    agent.setHeuristicRate(0.8)
    assert agent.epsilon == 0.9
    assert agent.heuristicRate == 0.8
