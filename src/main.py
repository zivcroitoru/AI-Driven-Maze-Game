# =========================
# file: src/main.py
# =========================
from __future__ import annotations

import argparse

from .core_types import MazeGenParams, TrainingConfig
from .maze_generator import MazeGenerator
from .environment import Environment
from .hybrid_agent import HybridAgent
from .logger import Logger
from .maze_ui import MazeUI
from .main_controller import MainController


def _parseArgs() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=300)
    p.add_argument("--evalEvery", type=int, default=50)

    p.add_argument("--rows", type=int, default=15)
    p.add_argument("--cols", type=int, default=15)
    p.add_argument("--wallDensity", type=float, default=0.25)
    p.add_argument("--seed", type=int, default=42)

    p.add_argument("--alpha", type=float, default=0.1)
    p.add_argument("--gamma", type=float, default=0.99)
    p.add_argument("--epsilon", type=float, default=0.25)
    p.add_argument("--heuristicRate", type=float, default=0.30)

    p.add_argument("--maxSteps", type=int, default=600)

    p.add_argument("--visual", type=int, default=0)
    p.add_argument("--interactive", type=int, default=1)
    p.add_argument("--cellSize", type=int, default=28)
    p.add_argument("--fps", type=int, default=60)

    p.add_argument("--logFile", type=str, default="./data/training_logs.csv")
    return p.parse_args()


def main() -> None:
    args = _parseArgs()

    genParams = MazeGenParams(
        rows=args.rows,
        cols=args.cols,
        wallDensity=args.wallDensity,
        seed=args.seed,
    )

    cfg = TrainingConfig(
        episodes=args.episodes,
        evalEvery=args.evalEvery,
        alpha=args.alpha,
        gamma=args.gamma,
        epsilon=args.epsilon,
        heuristicRate=args.heuristicRate,
        maxStepsPerEpisode=args.maxSteps,
        visual=bool(args.visual),
        interactive=bool(args.interactive),
        cellSize=args.cellSize,
        fps=args.fps,
        logFilePath=args.logFile,
    )

    mazeGen = MazeGenerator()
    grid, start, goal = mazeGen.generate(genParams)

    env = Environment(
        gridMatrix=grid,
        startPos=start,
        goalPos=goal,
        maxSteps=cfg.maxStepsPerEpisode,
    )

    agent = HybridAgent(
        alpha=cfg.alpha,
        gamma=cfg.gamma,
        epsilon=cfg.epsilon,
        heuristicRate=cfg.heuristicRate,
        seed=args.seed,
    )

    logger = Logger(cfg.logFilePath, console=True)

    ui = MazeUI(cellSize=cfg.cellSize, fps=cfg.fps) if cfg.visual else None

    controller = MainController(
        env=env,
        agent=agent,
        ui=ui,
        logger=logger,
        mazeGen=mazeGen,
    )

    controller.startTraining(cfg)


if __name__ == "__main__":
    main()
