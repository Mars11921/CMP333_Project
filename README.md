# Campus Robot

This project is the CMP 333 campus delivery robot scaffold.

The project is organized into phases so students can build the AI system gradually.

## Phase Roadmap

```text
Phase 1: Search strategies for pickup-and-delivery route planning
Phase 2: CSP scheduling for delivery assignment/order
Phase 3: HMM localization or MDP decision-making
```

The current implementation includes the visual simulator and the Phase 1 search scaffold.

## Setup

First, move into the project folder:

```bash
cd campus_robot
```

Create and activate a local virtual environment.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

Run the visual demo:

```bash
python run_visual_demo.py
```

Run the Phase 1 search check:

```bash
python phase1_search/check_phase1.py
```

Run the Phase 1 search visualization after implementing an algorithm:

```bash
python run_phase1_demo.py --source student --algorithm astar
```

---

**See phase1_search/README.md for phase1 deliverables**