# =========================
# file: src/environment.py
# =========================
from __future__ import annotations

from typing import Tuple
from .core_types import Grid, State, Action


class Environment:
    # UML fields:
    # - gridMatrix
    # - agentPos
    # - goalPos

    def __init__(self, gridMatrix: Grid, startPos: State, goalPos: State, maxSteps: int = 600) -> None:
        self.gridMatrix: Grid = gridMatrix
        self.agentPos: State = startPos
        self.goalPos: State = goalPos

        self._startPos: State = startPos
        self._maxSteps: int = maxSteps
        self._steps: int = 0
        self._done: bool = False

        # Reward function (as in doc)
        self._goalReward: float = 100.0
        self._collisionPenalty: float = -10.0
        self._stepPenalty: float = -1.0

    def reset(self) -> State:
        self.agentPos = self._startPos
        self._steps = 0
        self._done = False
        return self.agentPos

    def isValidMove(self, action: int) -> bool:
        if self._done:
            return False

        dr, dc = Action.delta(action)
        nr = self.agentPos[0] + dr
        nc = self.agentPos[1] + dc

        if nr < 0 or nc < 0:
            return False
        if nr >= len(self.gridMatrix) or nc >= len(self.gridMatrix[0]):
            return False

        return self.gridMatrix[nr][nc] == 0

    def step(self, action: int) -> Tuple[State, float, bool]:
        if self._done:
            return self.agentPos, 0.0, True

        self._steps += 1

        if self.isValidMove(action):
            dr, dc = Action.delta(action)
            self.agentPos = (self.agentPos[0] + dr, self.agentPos[1] + dc)

            if self.agentPos == self.goalPos:
                self._done = True
                return self.agentPos, self._goalReward, True

            if self._steps >= self._maxSteps:
                self._done = True
                return self.agentPos, self._stepPenalty, True

            return self.agentPos, self._stepPenalty, False

        # invalid move (collision)
        if self._steps >= self._maxSteps:
            self._done = True
            return self.agentPos, self._collisionPenalty, True

        return self.agentPos, self._collisionPenalty, False
