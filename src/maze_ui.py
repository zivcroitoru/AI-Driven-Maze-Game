# =========================
# file: src/maze_ui.py
# =========================
from __future__ import annotations

from typing import Any, Dict, Optional

from .core_types import Grid, MazeGenParams, State



class MazeUI:
    # UML methods:
    # - drawGrid(env)
    # - drawAgent(pos)
    # - updateScreen()

    def __init__(self, cellSize: int = 28, fps: int = 60) -> None:
        self._cellSize = cellSize
        self._fps = fps

        self._pygame = None
        self._screen = None
        self._clock = None
        self._font = None

        self._grid: Optional[Grid] = None
        self._agent: Optional[State] = None
        self._goal: Optional[State] = None

        # interactive controls state
        self._paused: bool = False
        self._stopRequested: bool = False
        self._restartEpisode: bool = False
        self._stepOnce: bool = False
        self._nextEpisode: bool = False
        self._fpsDelta: int = 0
        self._episodesDelta: int = 0

        self._lastHud: Dict[str, Any] = {}

    def _ensureInit(self, widthCells: int, heightCells: int) -> None:
        if self._pygame is not None:
            return

        import pygame  # lazy import

        self._pygame = pygame
        pygame.init()

        w = max(320, int(widthCells * self._cellSize))
        h = max(240, int(heightCells * self._cellSize + 90))  # HUD area

        self._screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("AI-Driven Maze Game")

        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("consolas", 18)

        # Make sure window becomes responsive immediately
        pygame.event.pump()
        pygame.display.flip()

    # ------------------------
    # Controls / Events
    # ------------------------
    def pollControls(self) -> Dict[str, Any]:
        """
        Returns one-shot control commands & persistent paused/stop flags.

        Keys:
          SPACE : pause/resume
          RIGHT : step one action (when paused)
          N     : run next episode (when paused at episode boundary)
          R     : restart current episode (immediate)
          Q/ESC : stop training
          +/=   : increase FPS
          -/_   : decrease FPS
          ]     : +10 episodes target
          [     : -10 episodes target (min 1)
        """
        # If controller calls this before init (before drawGrid), do not crash
        if self._pygame is None:
            return {
                "paused": self._paused,
                "stop": self._stopRequested,
                "restart_episode": False,
                "step_once": False,
                "next_episode": False,
                "fps_delta": 0,
                "episodes_delta": 0,
            }

        self._restartEpisode = False
        self._stepOnce = False
        self._nextEpisode = False
        self._fpsDelta = 0
        self._episodesDelta = 0

        for event in self._pygame.event.get():
            if event.type == self._pygame.QUIT:
                self._stopRequested = True

            if event.type == self._pygame.KEYDOWN:
                k = event.key

                if k in (self._pygame.K_q, self._pygame.K_ESCAPE):
                    self._stopRequested = True

                elif k == self._pygame.K_SPACE:
                    self._paused = not self._paused

                elif k == self._pygame.K_RIGHT:
                    self._stepOnce = True

                elif k == self._pygame.K_n:
                    self._nextEpisode = True

                elif k == self._pygame.K_r:
                    self._restartEpisode = True

                elif k in (self._pygame.K_PLUS, self._pygame.K_EQUALS, self._pygame.K_KP_PLUS):
                    self._fpsDelta = +10

                elif k in (self._pygame.K_MINUS, self._pygame.K_UNDERSCORE, self._pygame.K_KP_MINUS):
                    self._fpsDelta = -10

                elif k == self._pygame.K_RIGHTBRACKET:
                    self._episodesDelta = +10

                elif k == self._pygame.K_LEFTBRACKET:
                    self._episodesDelta = -10

        return {
            "paused": self._paused,
            "stop": self._stopRequested,
            "restart_episode": self._restartEpisode,
            "step_once": self._stepOnce,
            "next_episode": self._nextEpisode,
            "fps_delta": self._fpsDelta,
            "episodes_delta": self._episodesDelta,
        }

    def setHud(self, stats: Dict[str, Any]) -> None:
        self._lastHud = stats

    # ------------------------
    # UML rendering
    # ------------------------
    def drawGrid(self, env) -> None:
        grid = env.gridMatrix
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        self._ensureInit(cols, rows)

        self._grid = grid
        self._goal = env.goalPos

        self._screen.fill((20, 20, 20))

        for r in range(rows):
            for c in range(cols):
                x = c * self._cellSize
                y = r * self._cellSize

                color = (60, 60, 60) if grid[r][c] == 1 else (30, 30, 30)

                self._pygame.draw.rect(self._screen, color, (x, y, self._cellSize, self._cellSize))
                self._pygame.draw.rect(self._screen, (15, 15, 15), (x, y, self._cellSize, self._cellSize), 1)

        if self._goal is not None:
            gr, gc = self._goal
            gx = gc * self._cellSize
            gy = gr * self._cellSize
            self._pygame.draw.rect(self._screen, (0, 120, 0), (gx, gy, self._cellSize, self._cellSize))

        self._drawHudArea()

    def drawAgent(self, pos: State) -> None:
        self._agent = pos

        r, c = pos
        x = c * self._cellSize
        y = r * self._cellSize
        self._pygame.draw.rect(self._screen, (120, 50, 0), (x, y, self._cellSize, self._cellSize))

    def updateScreen(self) -> None:
        # Keep window responsive (especially on WSL/Wayland)
        self._pygame.event.pump()
        self._pygame.display.flip()
        self._clock.tick(self._fps)

    # ------------------------
    # HUD
    # ------------------------
    def _drawHudArea(self) -> None:
        if self._grid is None:
            return

        rows = len(self._grid)
        y0 = rows * self._cellSize

        self._pygame.draw.rect(self._screen, (10, 10, 10), (0, y0, self._screen.get_width(), 90))
        self._pygame.draw.line(self._screen, (30, 30, 30), (0, y0), (self._screen.get_width(), y0), 2)

        hud = self._lastHud or {}

        lines = [
            f"mode={hud.get('mode','?')}  ep={hud.get('episode','?')}/{hud.get('episodes_target','?')}  "
            f"t={hud.get('t','?')}  totalR={hud.get('total_reward','?')}  success={hud.get('success_rate','?')}%",
            f"alpha={hud.get('alpha','?')}  gamma={hud.get('gamma','?')}  eps={hud.get('epsilon','?')}  "
            f"heurRate={hud.get('heuristicRate','?')}  fps={self._fps}  paused={hud.get('paused', False)}",
            "keys: SPACE pause | RIGHT step | N next ep | R restart ep | +/- fps | [/] eps target | Q/ESC stop",
        ]

        for i, txt in enumerate(lines):
            surf = self._font.render(txt, True, (220, 220, 220))
            self._screen.blit(surf, (10, y0 + 10 + i * 24))
