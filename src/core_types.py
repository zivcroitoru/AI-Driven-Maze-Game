# =========================
# file: src/types.py
# =========================
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

State = Tuple[int, int]            # (row, col)
Grid = List[List[int]]             # 0 = free, 1 = wall
Path = List[State]


class Action:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    ALL = (UP, DOWN, LEFT, RIGHT)

    @staticmethod
    def delta(action: int) -> Tuple[int, int]:
        if action == Action.UP:
            return (-1, 0)
        if action == Action.DOWN:
            return (1, 0)
        if action == Action.LEFT:
            return (0, -1)
        if action == Action.RIGHT:
            return (0, 1)

        raise ValueError(f"Unknown action: {action}")


@dataclass
class MazeGenParams:
    rows: int = 15
    cols: int = 15
    wallDensity: float = 0.25
    seed: Optional[int] = 42
    maxTries: int = 250


@dataclass
class TrainingConfig:
    episodes: int = 300
    evalEvery: int = 50

    alpha: float = 0.1
    gamma: float = 0.99
    epsilon: float = 0.25
    heuristicRate: float = 0.30

    maxStepsPerEpisode: int = 600

    # UI
    visual: bool = False
    cellSize: int = 28
    fps: int = 60

    # interactive training controls (visual mode)
    interactive: bool = True

    # logging
    logFilePath: str = "training_logs.csv"
