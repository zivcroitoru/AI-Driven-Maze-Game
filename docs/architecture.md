# Architecture Overview

## System Architecture

The project follows a **Model–View–Controller (MVC)** architectural pattern.  
This design was chosen to ensure clear separation of concerns, modularity, and ease of testing.

The system is divided into three main layers:

- **Model** – Core logic and environment
- **View** – Visualization and user interaction
- **Controller** – Coordination of training, evaluation, and data flow

---

## Model Layer (Logic)

The Model layer contains all deterministic logic and algorithms.  
It is independent of visualization and user interaction.

### Components

- **Environment**
  - Represents the maze as a grid-world.
  - Manages agent position, rewards, terminal conditions, and step limits.
  - Provides a Gym-like API: `reset()` and `step(action)`.

- **HybridAgent**
  - Implements Q-learning.
  - Uses epsilon-greedy exploration.
  - Supports guided exploration using A* with a configurable probability.
  - Stores the Q-table as a mapping: `(state, action) → value`.

- **MazeGenerator**
  - Generates mazes using a seeded random process.
  - Controls maze size and wall density.
  - Ensures solvability by validating paths before training.

- **Pathfinder (A*)**
  - Stateless helper implementing the A* algorithm.
  - Uses Manhattan distance as the heuristic.
  - Can return either a full path or the next optimal move.

---

## View Layer (Presentation)

The View layer is responsible only for visualization and user input.

### Components

- **MazeUI**
  - Implemented using PyGame.
  - Renders the maze grid, agent, and goal.
  - Displays runtime statistics (episode, steps, reward, success rate).
  - Handles keyboard input in interactive mode.

The View layer does not contain any learning logic and does not modify the environment directly.

---

## Controller Layer (Coordination)

The Controller connects the Model and View layers and defines the runtime flow.

### Components

- **MainController**
  - Orchestrates training and evaluation loops.
  - Requests actions from the agent and applies them to the environment.
  - Sends environment state to the UI for rendering.
  - Logs steps and episode statistics.
  - Handles pause, resume, step-by-step execution, and stopping.

---

## Data Flow (Runtime)

1. The Controller initializes the environment and agent.
2. At each step:
   - The agent selects an action based on the current state.
   - The environment applies the action and returns the next state and reward.
   - The agent updates the Q-table (training mode only).
3. The Controller:
   - Logs step and episode data.
   - Updates the visualization if enabled.
4. Evaluation runs periodically with learning and exploration disabled.

---

## Design Rationale

- **Separation of concerns**  
  Learning logic, visualization, and control flow are isolated.

- **Deterministic and testable environment**  
  The environment can be tested independently of RL and UI.

- **Extensibility**  
  New agents, algorithms, or visualizations can be added without changing core logic.

- **Support for headless execution**  
  Enables fast training and automated evaluation without rendering.

---

## Summary

The MVC-based architecture ensures clarity, maintainability, and academic correctness.  
It allows fair comparison between pure reinforcement learning and hybrid learning with heuristic guidance, while keeping the system modular and easy to extend.
