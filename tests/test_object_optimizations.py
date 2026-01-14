import unittest
import timeit
import sys
import os

# Ensure NeditGD can be imported
sys.path.append(os.getcwd())

try:
    from NeditGD.object_gd import Object
except ImportError:
    sys.path.append(os.path.dirname(os.getcwd()))
    from NeditGD.object_gd import Object

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_performance(self):
        # Setup complex object
        data = {
            1: 1, 2: 100, 3: 200, 155: 1
        }
        for i in range(100):
            data[1000 + i] = f"value_{i}"

        obj = Object()
        obj.data.update(data)

        def run_to_robtop():
            obj.to_robtop()

        # Warmup
        run_to_robtop()

        # Benchmark
        number = 5000
        time_taken = timeit.timeit(run_to_robtop, number=number)
        avg_time = time_taken / number

        print(f"\n[Object.to_robtop] Time for {number} calls: {time_taken:.4f}s")
        print(f"[Object.to_robtop] Average time per call: {avg_time*1e6:.2f}µs")

        # Baseline was ~158µs. Optimized is ~137µs.
        # Set threshold at 250µs to be safe against CI fluctuations but catch major regressions.
        self.assertLess(avg_time, 0.000250, "Performance regression detected: Object.to_robtop is too slow")

    def test_to_robtop_correctness(self):
        obj = Object(id=1, x=10, y=20)
        # Expected properties: 1:1, 2:10, 3:20, 155:1

        robtop = obj.to_robtop()

        # Verify it's a string
        self.assertIsInstance(robtop, str)

        # Verify it doesn't end with comma
        self.assertFalse(robtop.endswith(','))

        # Verify round-trip
        obj2 = Object.from_robtop(robtop)
        self.assertEqual(obj[1], obj2[1])
        self.assertEqual(obj[2], obj2[2])
        self.assertEqual(obj[3], obj2[3])
        self.assertEqual(obj[155], obj2[155])

if __name__ == '__main__':
    unittest.main()
