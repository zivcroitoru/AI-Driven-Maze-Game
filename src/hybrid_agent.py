# =========================
# file: src/hybrid_agent.py
# =========================
from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import random

from core_types import Action, State
from environment import Environment
from pathfinder import Pathfinder


class HybridAgent:
    # UML fields:
    # - qTable
    # - alpha
    # - gamma
    # - epsilon
    # - heuristicRate
    # - pathfinder: Pathfinder

    # UML methods:
    # - getAction(state, env): Action
    # - updateQ(state, action, reward, nextState)

    def __init__(
        self,
        alpha: float,
        gamma: float,
        epsilon: float,
        heuristicRate: float,
        seed: Optional[int] = None,
    ) -> None:
        self.qTable: Dict[State, List[float]] = {}

        self.alpha: float = float(alpha)
        self.gamma: float = float(gamma)
        self.epsilon: float = float(epsilon)
        self.heuristicRate: float = float(heuristicRate)

        self.pathfinder: Pathfinder = Pathfinder()
        self._rng = random.Random(seed)

    def _ensureState(self, state: State) -> None:
        if state not in self.qTable:
            self.qTable[state] = [0.0, 0.0, 0.0, 0.0]

    def _argmaxAction(self, state: State) -> int:
        q = self.qTable[state]

        bestA = 0
        bestV = q[0]

        for a in (1, 2, 3):
            if q[a] > bestV:
                bestV = q[a]
                bestA = a

        return bestA

    def _validActions(self, env: Environment) -> List[int]:
        return [a for a in Action.ALL if env.isValidMove(a)]

    def getActionWithSource(self, state: State, env: Environment) -> Tuple[int, str]:
        self._ensureState(state)

        if self._rng.random() < self.epsilon:
            if self._rng.random() < self.heuristicRate:
                path = self.pathfinder.getAStarPath(env.gridMatrix, state, env.goalPos)

                if path:
                    a = self.pathfinder.nextMoveFromPath(path)

                    if a is not None and env.isValidMove(a):
                        return a, "astar"

            valid = self._validActions(env)

            if valid:
                return self._rng.choice(valid), "random_valid"

            return self._rng.choice(list(Action.ALL)), "random"

        return self._argmaxAction(state), "greedy"

    # UML method kept:
    def getAction(self, state: State, env: Environment) -> int:
        a, _ = self.getActionWithSource(state, env)
        return a

    def updateQ(self, state: State, action: int, reward: float, nextState: State) -> None:
        self._ensureState(state)
        self._ensureState(nextState)

        old = self.qTable[state][action]
        target = float(reward) + self.gamma * max(self.qTable[nextState])
        self.qTable[state][action] = old + self.alpha * (target - old)

    # optional helpers
    def setEpsilon(self, epsilon: float) -> None:
        self.epsilon = float(epsilon)

    def setHeuristicRate(self, heuristicRate: float) -> None:
        self.heuristicRate = float(heuristicRate)

    def resetQTable(self) -> None:
        self.qTable.clear()
