# AI-Driven Maze Game

## Name & Description
The **Hybrid AI Maze Solver** is a simulation and visualization system designed to train and evaluate autonomous agents within 2D grid mazes. It addresses "Sparse Reward" and "Inefficient Exploration" hurdles by combining Reinforcement Learning with deterministic pathfinding. The system is intended for pedagogical demonstrations, academic research, and benchmarking navigation algorithms in fields like robotics and logistics.

## Architecture
The system follows the **Model-View-Controller (MVC)** architectural pattern to ensure a strict separation of concerns.



[Image of Model-View-Controller architecture diagram]


* **Model (Logic Layer):** Encapsulates simulation data, environment rules, and decision-making intelligence, including the Hybrid Agent and A* module.
* **View (Presentation Layer):** A PyGame-based visualization component that renders the simulation state at 60 FPS.
* **Controller (Coordination Layer):** Orchestrates training/evaluation loops and handles data flow between the Model and View.
**Reasoning:** This decoupling allows the agent to be trained in a "Headless Mode" at maximum throughput without the overhead of real-time rendering.

## Technologies
* **Language:** Python 3.10+.
* **Graphics Engine:** PyGame.
* **Libraries:** NumPy (matrix operations), Pandas (data management), and Matplotlib (performance graphing).
* **Algorithms:** Q-Learning for adaptive behavior and A* for heuristic guidance.

## Installation & Execution
**Prerequisites:** Python 3.10+ and a standard hardware baseline (Intel i5/i7, 8GB RAM).

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/AI-Driven-Maze-Game.git](https://github.com/YOUR_USERNAME/AI-Driven-Maze-Game.git)
    cd AI-Driven-Maze-Game
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Project:**
    * **Visual Mode:** `python main.py --mode visual`
    * **Headless Mode:** `python main.py --mode headless`
4.  **Run Tests:**
    ```bash
    pytest tests/
    ```

## Project Structure
* **`/src`:** Core logic including the Hybrid Agent, A* Pathfinder, and Maze Environment.
* **`/assets`:** UI elements and sprites for the PyGame interface.
* **`/data`:** Persistent telemetry logs (`training_logs.csv`) and saved model weights (.npy/.json).
* **`/tests`:** Validation scripts for unit and integration testing.

## Usage
* **Guided Exploration:** During training, the agent can query the A* Pathfinder for a "Heuristic Teacher" move to accelerate convergence.
* **Model Persistence:** Trained Q-Tables can be saved and reloaded for evaluation sessions.
* **Deterministic Generation:** Uses seed-based generation to ensure reproducible maze layouts for research.

## Team
* **Ziv Croitoru** - Lead Developer.
* **Ilia Chirkov** - Developer.
* **Dennis Raev** - Developer.
* **Yonatan Shapira** - Developer.

## Status
* ✅ **Operational:** Hybrid Q-Learning/A* integration, seed-based maze generation, and MVC architectural integrity.
* 🚧 **In Development:** Multi-agent simulations, Deep Q-Networks (DQN), and dynamic obstacle environments.
