# Test Coverage Summary – AI Driven Maze Game

## Overview
This project includes a suite of automated tests to verify the correctness of the core modules.  
Tests are written using `pytest` and focus on functionality, edge cases, and expected behaviors of individual components.

---

## Tested Components

### environment.py
**Purpose:**  
Handles maze environment logic, including agent movement, collision detection, goal checking, and reward management.

**Tests include:**
- Environment reset behavior
- Valid and invalid moves
- Collision handling
- Reaching the goal
- Max steps termination
- Correct reward values

**Status:** Fully tested

---

### hybrid_agent.py
**Purpose:**  
Implements the hybrid reinforcement learning agent that combines Q-learning with A* heuristic search.

**Tests include:**
- Q-table initialization and updates
- Epsilon-greedy action selection
- Heuristic-based (A*) decisions
- Random vs greedy decisions
- Parameter updates (epsilon, heuristicRate)

**Status:** Fully tested

---

### pathfinder.py
**Purpose:**  
Provides A* pathfinding and movement extraction from path sequences.

**Tests include:**
- A* path correctness
- Action extraction from path
- Edge case handling (e.g., start == goal)

**Status:** Fully tested

---

### maze_generator.py
**Purpose:**  
Generates random mazes with configurable size and density, ensuring solvability.

**Tests include:**
- Maze shape and size
- Wall density control
- Start and goal location
- Ensuring solvable paths exist

**Status:** Fully tested

---

### core_types.py
**Purpose:**  
Defines common types, enums, and configuration data classes.

**Tests include:**
- Action-to-delta conversion
- Validity of Action.ALL
- Defaults in config classes

**Status:** Fully tested

---

### main_controller.py
**Purpose:**  
Coordinates training and evaluation loops using agent, environment, UI, and logging.

**Tests:**  
Covered indirectly through unit tests of its dependencies.  
No direct test needed unless UI behavior or full training flow is tested.

**Status:** Indirectly tested

---

### logger.py
**Purpose:**  
Handles CSV logging of training data.

**Tests:**  
Not directly tested; optional for full pipeline runs.

**Status:** Not tested
