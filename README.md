# Hybrid AI Maze Solver

A 2D simulation for training autonomous agents using Reinforcement Learning and A* pathfinding.

## 🏗 Architecture

The project uses the **Model-View-Controller (MVC)** pattern:

* **Model:** Handles simulation logic, Q-Learning, and A* pathfinding.
* **View:** PyGame-based 60 FPS rendering.
* **Controller:** Manages training loops and data flow.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Graphics:** PyGame
* **Data:** NumPy, Pandas, Matplotlib
* **Logic:** Q-Learning & A* Heuristics

---

## 🚀 Installation (Linux/WSL)

### 1. System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
sudo apt install -y libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 libfreetype6 libportmidi0

```

### 2. Virtual Environment & Python Libs

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pygame numpy pandas matplotlib

```

---

## 💻 Usage

Run from the **project root** directory:

| Mode | Command |
| --- | --- |
| **Headless (Fast)** | `python -m src.main` |
| **Visualized** | `python -m src.main --visual 1` |
| **Interactive** | `python -m src.main --visual 1 --interactive 1` |

### Key Arguments

* `--episodes N`: Training length (Default: 300).
* `--rows / --cols N`: Grid dimensions.
* `--wallDensity X`: Obstacle density (0.0 - 1.0).
* `--heuristicRate X`: Probability of A* guidance during exploration.
* `--alpha / --gamma`: RL learning rate and discount factor.

---

## 📂 Project Structure

```text
AI-Driven-Maze-Game/
├── src/      # Hybrid Logic, A*, Environment
├── tests/    # Unit and integration tests
├── docs/     # Technical specs
├── assets/   # PyGame sprites
└── data/     # Logs and saved Q-Tables

```

---

## 👥 Team

* **Denis Raev:** System Architect
* **Ziv Croitoru:** Algorithm Engineer
* **Ilia Chirkov:** Simulation Logic
* **Yehonatan Shapira:** UI/UX & QA
