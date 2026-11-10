#!/usr/bin/env python3
"""
Task: Formal Language and Automata-Based Real-World Problem Solving and System Design
Application: Infinite Loop Detection (Hybrid Static Ranking + State-Cycle Detection + Watchdog)
Author: S G S V GANESH
University: SRM Institute of Science and Technology
"""

from dataclasses import dataclass
from typing import Callable, Dict, Tuple


@dataclass
class LoopProgram:
    name: str
    init_state: Dict[str, int]
    condition_fn: Callable[[Dict[str, int]], bool]
    step_fn: Callable[[Dict[str, int]], Dict[str, int]]
    static_var: str
    bound_dir: str      # "decreasing_to_zero" or "increasing_to_limit" or "complex"
    static_delta: int   # Expected change per step (0 if non-monotonic/complex)


class HybridLoopAnalyzer:
    def __init__(self, max_steps: int = 150):
        self.max_steps = max_steps

    def analyze_and_execute(self, prog: LoopProgram) -> Tuple[str, str]:
        # TIER 1: Static Ranking Function Check
        static_note = "Static Check: Inconclusive (Non-monotonic or dynamic update)"
        if prog.bound_dir == "decreasing_to_zero" and prog.static_delta < 0:
            static_note = "Static Check: PROVEN TERMINATING (Well-founded decreasing variant)"
        elif prog.bound_dir == "increasing_to_limit" and prog.static_delta > 0:
            static_note = "Static Check: PROVEN TERMINATING (Monotonic progress to upper bound)"
        elif prog.static_delta == 0 and prog.bound_dir in ("decreasing_to_zero", "increasing_to_limit"):
            static_note = "Static Check: WARNING (Zero progress delta detected statically)"

        # TIER 2 & 3: Configuration Cycle Detection + Bounded Watchdog Execution
        state = dict(prog.init_state)
        visited_configs = set()
        steps = 0
        trace_preview = []

        while prog.condition_fn(state):
            config_signature = tuple(sorted(state.items()))
            if len(trace_preview) < 5:
                trace_preview.append(str(dict(config_signature)))

            # Tier 2: Exact Configuration Repetition -> Guaranteed Infinite Loop
            if config_signature in visited_configs:
                trace_str = " -> ".join(trace_preview) + f" -> {dict(config_signature)} [REPEAT]"
                return (
                    "INFINITE_LOOP_CYCLE",
                    f"{static_note} | Runtime: Exact state repeat at step {steps} ({trace_str})"
                )

            visited_configs.add(config_signature)

            # Tier 3: Bounded Watchdog Cutoff
            if steps >= self.max_steps:
                trace_str = " -> ".join(trace_preview) + " -> ..."
                return (
                    "WATCHDOG_TIMEOUT",
                    f"{static_note} | Runtime: Exceeded K_max={self.max_steps} steps without repeating state ({trace_str})"
                )

            state = prog.step_fn(dict(state))
            steps += 1

        trace_str = " -> ".join(trace_preview) + f" -> {state} [EXIT]"
        return (
            "TERMINATED_NORMALLY",
            f"{static_note} | Runtime: Halted cleanly in {steps} steps ({trace_str})"
        )


def build_test_cases():
    return [
        LoopProgram(
            name="1. Valid Countdown Loop (n=15, step=-3)",
            init_state={"n": 15},
            condition_fn=lambda s: s["n"] > 0,
            step_fn=lambda s: {"n": s["n"] - 3},
            static_var="n",
            bound_dir="decreasing_to_zero",
            static_delta=-3,
        ),
        LoopProgram(
            name="2. Modular Cycle Bug (x=1, x=(x+2)%4 != 0)",
            init_state={"x": 1},
            condition_fn=lambda s: s["x"] != 0,
            step_fn=lambda s: {"x": (s["x"] + 2) % 4},
            static_var="x",
            bound_dir="complex",
            static_delta=0,
        ),
        LoopProgram(
            name="3. Stagnant Bug Loop (i=0, i<10, step=0)",
            init_state={"i": 0},
            condition_fn=lambda s: s["i"] < 10,
            step_fn=lambda s: {"i": s["i"]},
            static_var="i",
            bound_dir="increasing_to_limit",
            static_delta=0,
        ),
        LoopProgram(
            name="4. Runaway State Growth (n=1, n>0, step=+1)",
            init_state={"n": 1},
            condition_fn=lambda s: s["n"] > 0,
            step_fn=lambda s: {"n": s["n"] + 1},
            static_var="n",
            bound_dir="decreasing_to_zero",
            static_delta=1,
        ),
        LoopProgram(
            name="5. Collatz Sequence (n=27, non-monotonic hailstone)",
            init_state={"n": 27},
            condition_fn=lambda s: s["n"] > 1,
            step_fn=lambda s: {"n": s["n"] // 2 if s["n"] % 2 == 0 else 3 * s["n"] + 1},
            static_var="n",
            bound_dir="complex",
            static_delta=0,
        ),
    ]


if __name__ == "__main__":
    analyzer = HybridLoopAnalyzer(max_steps=150)
    print("=" * 105)
    print(" FORMAL COMPUTABILITY & HYBRID INFINITE-LOOP DETECTION DEMONSTRATION")
    print("=" * 105)
    for prog in build_test_cases():
        verdict, detail = analyzer.analyze_and_execute(prog)
        print(f"\nProgram : {prog.name}")
        print(f"Verdict : [{verdict}]")
        print(f"Analysis: {detail}")