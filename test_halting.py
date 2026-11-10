import unittest
from halting_loop_analyzer import HybridLoopAnalyzer, build_test_cases

class TestHaltingLoopAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = HybridLoopAnalyzer(max_steps=150)
        self.cases = {prog.name: prog for prog in build_test_cases()}

    def test_countdown_terminates(self):
        prog = self.cases["1. Valid Countdown Loop (n=15, step=-3)"]
        verdict, _ = self.analyzer.analyze_and_execute(prog)
        self.assertEqual(verdict, "TERMINATED_NORMALLY")

    def test_modular_cycle_detected(self):
        prog = self.cases["2. Modular Cycle Bug (x=1, x=(x+2)%4 != 0)"]
        verdict, _ = self.analyzer.analyze_and_execute(prog)
        self.assertEqual(verdict, "INFINITE_LOOP_CYCLE")

    def test_stagnant_loop_detected(self):
        prog = self.cases["3. Stagnant Bug Loop (i=0, i<10, step=0)"]
        verdict, _ = self.analyzer.analyze_and_execute(prog)
        self.assertEqual(verdict, "INFINITE_LOOP_CYCLE")

    def test_runaway_growth_timeout(self):
        prog = self.cases["4. Runaway State Growth (n=1, n>0, step=+1)"]
        verdict, _ = self.analyzer.analyze_and_execute(prog)
        self.assertEqual(verdict, "WATCHDOG_TIMEOUT")

    def test_collatz_terminates(self):
        prog = self.cases["5. Collatz Sequence (n=27, non-monotonic hailstone)"]
        verdict, _ = self.analyzer.analyze_and_execute(prog)
        self.assertEqual(verdict, "TERMINATED_NORMALLY")

if __name__ == "__main__":
    unittest.main(verbosity=2)