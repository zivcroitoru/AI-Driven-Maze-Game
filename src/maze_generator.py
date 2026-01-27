# =========================
# file: src/maze_generator.py
# =========================
from __future__ import annotations

from typing import Tuple
import random

from .core_types import Grid, MazeGenParams, State
from .pathfinder import Pathfinder


class MazeGenerator:
    # UML methods:
    # - generate(params): Grid
    # - ensureSolvable(grid, start, goal): bool

    def __init__(self) -> None:
        self._pathfinder = Pathfinder()

    def generate(self, params: MazeGenParams) -> Tuple[Grid, State, State]:
        rng = random.Random(params.seed)

        start: State = (0, 0)
        goal: State = (params.rows - 1, params.cols - 1)

        for _ in range(params.maxTries):
            grid: Grid = [[0 for _ in range(params.cols)] for _ in range(params.rows)]

            for r in range(params.rows):
                for c in range(params.cols):
                    if rng.random() < params.wallDensity:
                        grid[r][c] = 1

            grid[start[0]][start[1]] = 0
            grid[goal[0]][goal[1]] = 0

            if self.ensureSolvable(grid, start, goal):
                return grid, start, goal

        grid = [[0 for _ in range(params.cols)] for _ in range(params.rows)]
        return grid, start, goal

    def ensureSolvable(self, grid: Grid, start: State, goal: State) -> bool:
        path = self._pathfinder.getAStarPath(grid, start, goal)
        return path is not None
