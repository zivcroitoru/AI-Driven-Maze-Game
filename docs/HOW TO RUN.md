\## Linux / WSL (Ubuntu/Debian) — Installation and Run Instructions



\### 1) Install system dependencies

Open a terminal in the project root directory and run:



1\) sudo apt update

2\) sudo apt install -y python3 python3-venv python3-pip

3\) (Required for PyGame rendering)

&nbsp;  sudo apt install -y \\

&nbsp;    libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \\

&nbsp;    libfreetype6 libportmidi0



---



\### 2) Create and activate a virtual environment

IMPORTANT: All commands below must be executed from the project root directory

(the directory that contains the `src/` folder).



4\) python3 -m venv venv  

5\) source venv/bin/activate  

6\) pip install --upgrade pip  

7\) pip install pygame  

&nbsp;  (If used by the project: `pip install numpy pandas matplotlib`)



Verification:

\- `which python` → should point to `.../project/venv/bin/python`

\- `python -c "import pygame; print(pygame.\_\_version\_\_)"` → should print the version without errors



---



\### 3) Run the application (from project root only)



Headless mode (no graphics, fastest):

\- python -m src.main



With visualization (PyGame window):

\- python -m src.main --visual 1



With visualization and interactive controls:

\- python -m src.main --visual 1 --interactive 1



---



\## Command-Line Arguments



--visual 0/1  

&nbsp; 0 = no rendering (headless mode), 1 = enable PyGame visualization



--interactive 0/1  

&nbsp; 0 = no user interaction, 1 = enable keyboard controls (if visualization is enabled)



--episodes N  

&nbsp; Number of training episodes (default: 300)



--evalEvery N  

&nbsp; Run evaluation every N episodes (0 disables evaluation)



--rows N, --cols N  

&nbsp; Maze dimensions (e.g., 15x15)



--wallDensity X  

&nbsp; Obstacle density in the maze (e.g., 0.25)



--seed N  

&nbsp; Random seed for reproducible experiments



--alpha X  

&nbsp; Q-learning learning rate



--gamma X  

&nbsp; Discount factor for future rewards



--epsilon X  

&nbsp; Exploration probability (epsilon-greedy)



--heuristicRate X  

&nbsp; Probability of guided exploration using A\* during exploration



--maxSteps N  

&nbsp; Maximum steps per episode (prevents infinite loops)



--cellSize N  

&nbsp; Cell size in pixels (visual mode only)



--fps N  

&nbsp; Rendering speed (frames per second)



--logFile PATH  

&nbsp; Path to CSV log file (e.g., training\_logs\_steps.csv)



---



\## Example Runs



1\) Visualization with interactive control:

&nbsp;  python -m src.main --visual 1 --interactive 1



2\) Fast headless training (1000 episodes):

&nbsp;  python -m src.main --visual 0 --episodes 1000



3\) Custom maze size and wall density:

&nbsp;  python -m src.main --rows 20 --cols 20 --wallDensity 0.30 --seed 42



4\) Custom reinforcement learning parameters:

&nbsp;  python -m src.main --alpha 0.1 --gamma 0.99 --epsilon 0.25 --heuristicRate 0.30

---

## 🧪 Running Unit Tests

All automated tests are located in the `tests/` directory and use **pytest**.

---

### 1. Activate the virtual environment

From the project root directory, run:

```bash
source venv/bin/activate 
```
Note: If the virtual environment does not exist yet, create it first:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pytest
```
### 2. Run all tests
Make sure you are in the project root directory, then run:
```bash
PYTHONPATH=src pytest -v tests/
```

### 3. Run a single test file
Example:
```bash
PYTHONPATH=src pytest -v tests test_environment.py
```
### 4. Expected Output
If everything works correctly, you should see output similar to this:
```bash
================== test session starts ==================
collected 4 items

tests/test_environment.py ..... PASSED
tests/test_maze_generator.py ... PASSED
tests/test_pathfinder.py ..... PASSED
tests/test_hybrid_agent.py .... PASSED

================== 4 passed in 0.45s ====================
```