# Infinite Loop Detection & Halting Analysis

**Author:** S G S V GANESH  
**University:** SRM Institute of Science and Technology  

This repository investigates the undecidability of infinite loop detection (The Halting Problem $HALT_{\text{TM}}$) and provides a practical, three-tier hybrid engineering solution: **Static Ranking Function Verification**, **Configuration Cycle Detection**, and **Bounded Watchdog Execution**.

---

## 1. Theoretical Analysis
* **Undecidability:** By reduction from $HALT_{\text{TM}}$, no general algorithm can decide whether an arbitrary program halts on all inputs.
* **Recognizability:** $HALT_{\text{TM}}$ is Turing-recognizable (semi-decidable), while $LOOP_{\text{TM}}$ is co-Turing-recognizable.
* **Engineering Workaround:** Real-time systems enforce decidability by combining static monotonicity verification, finite-state memoization, and $K_{\max}$ step limits (watchdogs).

---

## 2. Project Structure
* `halting_loop_analyzer.py` - Core Python hybrid analysis engine.
* `test_halting.py` - Automated unit tests.
* `index.html` - Interactive web simulator.

---

## 3. How to Run Locally

```bash
# Run the Python engine demonstration
python halting_loop_analyzer.py

# Run the automated unit tests
python test_halting.py
