# =========================
# file: src/logger.py
# =========================
from __future__ import annotations

import csv
import os
import time


class Logger:
    # UML fields:
    # - filePath
    # UML methods:
    # - logStep(...)
    # - logEpisode(...)
    # - flush()

    def __init__(self, filePath: str, console: bool = True) -> None:
        self.filePath: str = filePath
        self.console: bool = console

        self._stepFile = None
        self._episodeFile = None

        self._stepWriter = None
        self._episodeWriter = None

        self._t0 = time.time()

        self._open()

    def _withSuffix(self, base: str, suffix: str) -> str:
        root, ext = os.path.splitext(base)
        if not ext:
            ext = ".csv"
        return f"{root}{suffix}"

    def _open(self) -> None:
        stepPath = self._withSuffix(self.filePath, "_steps.csv")
        epPath = self._withSuffix(self.filePath, "_episodes.csv")

        newSteps = not os.path.exists(stepPath)
        newEps = not os.path.exists(epPath)

        self._stepFile = open(stepPath, "a", newline="", encoding="utf-8")
        self._episodeFile = open(epPath, "a", newline="", encoding="utf-8")

        self._stepWriter = csv.writer(self._stepFile)
        self._episodeWriter = csv.writer(self._episodeFile)

        if newSteps:
            self._stepWriter.writerow(
                ["episode", "t", "state_r", "state_c", "action", "reward", "done", "mode", "source"]
            )

        if newEps:
            self._episodeWriter.writerow(
                ["episode", "steps", "total_reward", "success", "mode", "elapsed_s"]
            )

    def info(self, msg: str) -> None:
        if self.console:
            print(msg, flush=True)

    def logStep(
        self,
        episode: int,
        t: int,
        state_r: int,
        state_c: int,
        action: int,
        reward: float,
        done: bool,
        mode: str,
        source: str,
    ) -> None:
        self._stepWriter.writerow(
            [episode, t, state_r, state_c, action, reward, int(done), mode, source]
        )

    def logEpisode(
        self,
        episode: int,
        steps: int,
        total_reward: float,
        success: bool,
        mode: str,
    ) -> None:
        elapsed = time.time() - self._t0
        self._episodeWriter.writerow(
            [episode, steps, total_reward, int(success), mode, round(elapsed, 3)]
        )

    def flush(self) -> None:
        if self._stepFile:
            self._stepFile.flush()

        if self._episodeFile:
            self._episodeFile.flush()
