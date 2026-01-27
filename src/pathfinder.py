# =========================
# file: src/pathfinder.py
# =========================
from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import heapq

from core_types import Action, Grid, Path, State



class Pathfinder:
    def _inBounds(self, grid: Grid, s: State) -> bool:
        r, c = s
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def _isFree(self, grid: Grid, s: State) -> bool:
        r, c = s
        return grid[r][c] == 0

    def _neighbors(self, grid: Grid, s: State) -> List[Tuple[State, int]]:
        out: List[Tuple[State, int]] = []

        for a in Action.ALL:
            dr, dc = Action.delta(a)
            ns = (s[0] + dr, s[1] + dc)
            if self._inBounds(grid, ns) and self._isFree(grid, ns):
                out.append((ns, a))

        return out

    def _manhattan(self, a: State, b: State) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # UML methods:
    # - getAStarPath(grid, start, goal): Path
    # - nextMoveFromPath(path): Action
    def getAStarPath(self, grid: Grid, start: State, goal: State) -> Optional[Path]:
        if start == goal:
            return [start]

        openHeap: List[Tuple[int, int, State]] = []
        heapq.heappush(openHeap, (0, 0, start))

        cameFrom: Dict[State, State] = {}
        gScore: Dict[State, int] = {start: 0}
        closed = set()

        while openHeap:
            # IMPORTANT: heappop takes exactly one argument
            _, g, cur = heapq.heappop(openHeap)

            if cur in closed:
                continue
            closed.add(cur)

            if cur == goal:
                return self._reconstruct(cameFrom, cur)

            for ns, _ in self._neighbors(grid, cur):
                ng = g + 1
                if ns not in gScore or ng < gScore[ns]:
                    gScore[ns] = ng
                    cameFrom[ns] = cur
                    f = ng + self._manhattan(ns, goal)
                    heapq.heappush(openHeap, (f, ng, ns))

        return None

    def _reconstruct(self, cameFrom: Dict[State, State], cur: State) -> Path:
        path: Path = [cur]
        while cur in cameFrom:
            cur = cameFrom[cur]
            path.append(cur)
        path.reverse()
        return path

    def nextMoveFromPath(self, path: Optional[Path]) -> Optional[int]:
        if not path or len(path) < 2:
            return None

        cur = path[0]
        nxt = path[1]

        dr = nxt[0] - cur[0]
        dc = nxt[1] - cur[1]

        if (dr, dc) == (-1, 0):
            return Action.UP
        if (dr, dc) == (1, 0):
            return Action.DOWN
        if (dr, dc) == (0, -1):
            return Action.LEFT
        if (dr, dc) == (0, 1):
            return Action.RIGHT

        return None
