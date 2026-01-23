## 1. Functional Requirements

* **Maze Generation:** The system shall create $N \times M$ grids with static obstacles (walls), a single start cell, and a single goal cell.
* **Reachability Validation:** The system must verify that a valid path exists between the start and goal using the Pathfinder module before training begins.
* **Hybrid AI Navigation Policy:**
    * **Core Learning:** Implementation of a Q-Learning agent using a tabular Q-Table to learn action values for each discrete state.
    * **Guided Exploration:** Use of the A* algorithm as a heuristic guidance mechanism during exploration to bias the agent toward promising directions.
* **Execution Modes:**
    * **Training Mode:** Enables learning, exploration, and optional A* guidance.
    * **Evaluation Mode:** Disables learning and A* guidance to measure the learned policy's performance in isolation.
* **Visualization:** A graphical interface using PyGame to display the maze, agent position, and episode statistics in real-time.
* **Data Logging:** Automatic saving of training metrics including steps, total reward, success rate, and path efficiency to CSV files.

---

## 2. User Stories & Use Cases

### User Stories
* **As a Student:** I want to watch the agent learn in real-time through a GUI so I can understand the relationship between rewards and agent movement.
* **As a Researcher:** I want to run the system in headless mode to maximize training speed and throughput.
* **As a Researcher:** I want to compare "Pure Q-Learning" vs. "Hybrid AI" to measure improvements in learning speed and path optimality.

### Primary Use Cases

**UC-1: Configure Maze and Start Training**
The user opens the configuration panel to set maze and training parameters. Once "Start Training" is clicked, the system generates the maze, initializes the agent, and begins the training loop across multiple episodes.


**UC-2: Run Evaluation Episode with Trained Agent**
The user selects "Evaluation Mode" and chooses a seed type. The system loads the trained policy from storage and runs evaluation episodes without learning or exploration to provide success results and trajectory metrics.

---

## 3. Interaction & Logic Flow

### Training Logic Flow

The training cycle follows a discrete-time control cycle governed by the Markov Decision Process (MDP):
1. **Observation:** The Agent identifies the current state (coordinates) from the Environment.
2. **Action Selection:** The Agent chooses between Exploitation (Q-Table) or Exploration (Random move or A* Guided via the Integration Layer).
3. **Execution:** The selected action is sent to the Environment, which returns the next state, outcome, and reward.
4. **Q-Update:** The Agent updates the policy using the Bellman Equation based on the reward and future value.
5. **Logging:** Step and episode metrics are recorded in real-time for later analysis.

### Evaluation Logic Flow

To measure true performance, the evaluation flow uses a fixed policy:
* **Consistency:** The system ensures consistent environment reset behavior across test mazes.
* **Metrics:** The system records success rate, average steps to goal, and path efficiency to compare against A* baselines.

---

## 4. Non-Functional Requirements

### Performance & Scalability
* **Decision Latency:** The agent must calculate a move in < 5ms in Headless Mode and < 16ms in Visual Mode to maintain 60 FPS.
* **Maze Size:** The system must handle grids up to $25 \times 25$ without performance lag.
* **Learning Efficiency:** The Hybrid Agent is hypothesized to learn 30% faster than a standard agent.

### Technical Constraints
* **Hardware:** Optimized for standard student laptops (Intel i5/i7, 8GB RAM) with no GPU requirement.
* **Software Stack:** Developed in Python 3.10+ using NumPy for calculations, PyGame for visuals, and Pandas for data analysis.
* **Reliability:** Data is appended to `training_logs.csv` immediately upon episode termination to prevent loss during a crash.
