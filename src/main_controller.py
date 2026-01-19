# =========================
# file: src/main_controller.py
# =========================
from __future__ import annotations

from collections import deque
from typing import Any, Dict, Optional

from .environment import Environment
from .hybrid_agent import HybridAgent
from .logger import Logger
from .maze_generator import MazeGenerator
from .maze_ui import MazeUI
from .core_types import TrainingConfig


class MainController:
    # UML fields:
    # - env: Environment
    # - agent: HybridAgent
    # - ui: MazeUI
    # - logger: Logger
    # - mazeGen: MazeGenerator

    def __init__(
        self,
        env: Environment,
        agent: HybridAgent,
        ui: Optional[MazeUI],
        logger: Optional[Logger],
        mazeGen: Optional[MazeGenerator],
    ) -> None:
        self.env: Environment = env
        self.agent: HybridAgent = agent
        self.ui: Optional[MazeUI] = ui
        self.logger: Optional[Logger] = logger
        self.mazeGen: Optional[MazeGenerator] = mazeGen

        self._episodeId: int = 0
        self._episodesTarget: int = 0

        self._stopRequested: bool = False
        self._paused: bool = False

        # rolling stats
        self._recentSuccess = deque(maxlen=50)
        self._recentRewards = deque(maxlen=50)
        self._recentSteps = deque(maxlen=50)

        # ui one-shot flags
        self._restartEpisodeFlag: bool = False
        self._stepOnceFlag: bool = False
        self._nextEpisodeGate: bool = False

    # UML methods:
    # - startTraining(config)
    # - runEpisode()
    # - runEvaluation()
    def startTraining(self, config: TrainingConfig) -> None:
        self._episodesTarget = max(1, int(config.episodes))

        if self.logger:
            self.logger.info(
                f"[SYSTEM] startTraining: episodes={self._episodesTarget}, evalEvery={config.evalEvery}, "
                f"alpha={config.alpha}, gamma={config.gamma}, epsilon={config.epsilon}, "
                f"heuristicRate={config.heuristicRate}, visual={config.visual}, interactive={config.interactive}"
            )

        ep = 0
        while ep < self._episodesTarget and not self._stopRequested:
            self._episodeId = ep + 1

            res = self.runEpisode(config)

            self._recentSuccess.append(1 if res["success"] else 0)
            self._recentRewards.append(res["total_reward"])
            self._recentSteps.append(res["steps"])

            if self.logger:
                sr = int(round(100.0 * (sum(self._recentSuccess) / max(1, len(self._recentSuccess)))))
                self.logger.info(
                    f"[TRAIN] ep={res['episode']}/{self._episodesTarget} steps={res['steps']} "
                    f"reward={res['total_reward']:.1f} success={res['success']} recentSR={sr}%"
                )

            if config.evalEvery > 0 and (self._episodeId % config.evalEvery == 0) and not self._stopRequested:
                ev = self.runEvaluation(config)
                if self.logger:
                    self.logger.info(
                        f"[EVAL ] ep={ev['episode']} steps={ev['steps']} "
                        f"reward={ev['total_reward']:.1f} success={ev['success']}"
                    )

            ep += 1

            # if interactive + paused, allow "next episode" gating
            if config.visual and config.interactive and self.ui:
                while self._paused and not self._stopRequested:
                    self._handleUIControls(config, mode="train", episode=self._episodeId, t=0, totalReward=0.0)

                    self._renderHUD(config, mode="train", episode=self._episodeId, t=0, totalReward=0.0)
                    self.ui.drawGrid(self.env)
                    self.ui.drawAgent(self.env.agentPos)
                    self.ui.updateScreen()

                    if self._nextEpisodeGate:
                        self._nextEpisodeGate = False
                        break

        if self.logger:
            self.logger.info("[SYSTEM] training finished -> flushing logs...")
            self.logger.flush()

    def runEpisode(self, config: TrainingConfig) -> Dict[str, Any]:
        mode = "train"
        state = self.env.reset()
        totalReward = 0.0
        steps = 0

        # FIX: ensure window is created and visible BEFORE pollControls()
        if config.visual and self.ui:
            self._renderHUD(config, mode=mode, episode=self._episodeId, t=0, totalReward=0.0)
            self.ui.drawGrid(self.env)
            self.ui.drawAgent(self.env.agentPos)
            self.ui.updateScreen()

        while True:
            if config.visual and config.interactive and self.ui:
                self._handleUIControls(config, mode=mode, episode=self._episodeId, t=steps, totalReward=totalReward)

                if self._stopRequested:
                    return {
                        "episode": self._episodeId,
                        "steps": steps,
                        "total_reward": totalReward,
                        "success": False,
                    }

                if self._restartEpisodeFlag:
                    self._restartEpisodeFlag = False
                    state = self.env.reset()
                    totalReward = 0.0
                    steps = 0

                if self._paused and not self._stepOnceFlag:
                    self._renderHUD(config, mode=mode, episode=self._episodeId, t=steps, totalReward=totalReward)
                    self.ui.drawGrid(self.env)
                    self.ui.drawAgent(self.env.agentPos)
                    self.ui.updateScreen()
                    continue

            if self.ui:
                self._renderHUD(config, mode=mode, episode=self._episodeId, t=steps, totalReward=totalReward)
                self.ui.drawGrid(self.env)
                self.ui.drawAgent(self.env.agentPos)
                self.ui.updateScreen()

            action, source = self.agent.getActionWithSource(state, self.env)
            nextState, reward, done = self.env.step(action)

            self.agent.updateQ(state, action, reward, nextState)

            totalReward += reward
            steps += 1

            if self.logger:
                self.logger.logStep(
                    episode=self._episodeId,
                    t=steps,
                    state_r=state[0],
                    state_c=state[1],
                    action=action,
                    reward=reward,
                    done=done,
                    mode=mode,
                    source=source,
                )

            state = nextState

            if self._stepOnceFlag:
                self._stepOnceFlag = False

            if done:
                success = (self.env.agentPos == self.env.goalPos)
                if self.logger:
                    self.logger.logEpisode(
                        episode=self._episodeId,
                        steps=steps,
                        total_reward=totalReward,
                        success=success,
                        mode=mode,
                    )
                return {
                    "episode": self._episodeId,
                    "steps": steps,
                    "total_reward": totalReward,
                    "success": success,
                }

    def runEvaluation(self, config: TrainingConfig) -> Dict[str, Any]:
        mode = "eval"

        oldEps = self.agent.epsilon
        oldHR = self.agent.heuristicRate

        self.agent.epsilon = 0.0
        self.agent.heuristicRate = 0.0

        state = self.env.reset()
        totalReward = 0.0
        steps = 0

        if config.visual and self.ui:
            self._renderHUD(config, mode=mode, episode=100000 + self._episodeId, t=0, totalReward=0.0)
            self.ui.drawGrid(self.env)
            self.ui.drawAgent(self.env.agentPos)
            self.ui.updateScreen()

        while True:
            if config.visual and self.ui:
                if config.interactive:
                    self._handleUIControls(
                        config,
                        mode=mode,
                        episode=100000 + self._episodeId,
                        t=steps,
                        totalReward=totalReward,
                    )
                    if self._stopRequested:
                        break

                self._renderHUD(config, mode=mode, episode=100000 + self._episodeId, t=steps, totalReward=totalReward)
                self.ui.drawGrid(self.env)
                self.ui.drawAgent(self.env.agentPos)
                self.ui.updateScreen()

            action, _ = self.agent.getActionWithSource(state, self.env)
            nextState, reward, done = self.env.step(action)

            totalReward += reward
            steps += 1
            state = nextState

            if done:
                break

        success = (self.env.agentPos == self.env.goalPos)

        if self.logger:
            self.logger.logEpisode(
                episode=100000 + self._episodeId,
                steps=steps,
                total_reward=totalReward,
                success=success,
                mode=mode,
            )

        self.agent.epsilon = oldEps
        self.agent.heuristicRate = oldHR

        return {
            "episode": 100000 + self._episodeId,
            "steps": steps,
            "total_reward": totalReward,
            "success": success,
        }

    # ------------------------
    # Internal helpers
    # ------------------------
    def _handleUIControls(self, config: TrainingConfig, mode: str, episode: int, t: int, totalReward: float) -> None:
        if not self.ui:
            return

        cmd = self.ui.pollControls()

        self._paused = bool(cmd["paused"])
        self._stopRequested = bool(cmd["stop"])

        fps_delta = int(cmd["fps_delta"])
        if fps_delta != 0:
            self.ui._fps = max(10, min(240, self.ui._fps + fps_delta))

        eps_delta = int(cmd["episodes_delta"])
        if eps_delta != 0:
            self._episodesTarget = max(1, self._episodesTarget + eps_delta)
            if self.logger:
                self.logger.info(f"[SYSTEM] episodes target updated -> {self._episodesTarget}")

        if cmd["restart_episode"]:
            self._restartEpisodeFlag = True

        if cmd["step_once"]:
            self._stepOnceFlag = True

        if cmd["next_episode"]:
            self._nextEpisodeGate = True

    def _renderHUD(self, config: TrainingConfig, mode: str, episode: int, t: int, totalReward: float) -> None:
        if not self.ui:
            return

        sr = int(round(100.0 * (sum(self._recentSuccess) / max(1, len(self._recentSuccess))))) if self._recentSuccess else 0

        hud = {
            "mode": mode,
            "episode": episode if mode != "train" else self._episodeId,
            "episodes_target": self._episodesTarget,
            "t": t,
            "total_reward": f"{totalReward:.1f}",
            "success_rate": sr,
            "alpha": f"{config.alpha}",
            "gamma": f"{config.gamma}",
            "epsilon": f"{self.agent.epsilon:.3f}",
            "heuristicRate": f"{self.agent.heuristicRate:.3f}",
            "paused": self._paused,
        }

        self.ui.setHud(hud)
