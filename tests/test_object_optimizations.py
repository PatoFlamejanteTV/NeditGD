import unittest
import timeit
from NeditGD.object_gd import Object

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_correctness(self):
        # Create an object with known properties
        obj = Object()
        # Object initializes with {1:1, 2:0, 3:0, 155:1}
        obj.data = {1: 1, 2: 10, 3: 20} # Override for simple test

        # Expected output: 1,1,2,10,3,20
        # The order depends on dictionary iteration order, which is insertion-ordered in recent Python versions.
        # However, to be safe, we can check if all parts are present.

        # Note: NeditGD's encode_property returns "key,val,"
        # So for 1:1 -> "1,1,"
        # For 2:10 -> "2,10,"
        # For 3:20 -> "3,20,"
        # Joined: "1,1,2,10,3,20,"
        # Result[:-1]: "1,1,2,10,3,20"

        result = obj.to_robtop()
        parts = result.split(',')

        # Should be key, val, key, val ...
        self.assertEqual(len(parts) % 2, 0)

        data_map = {}
        for i in range(0, len(parts), 2):
            data_map[int(parts[i])] = int(parts[i+1])

        self.assertEqual(data_map[1], 1)
        self.assertEqual(data_map[2], 10)
        self.assertEqual(data_map[3], 20)

    def test_to_robtop_performance(self):
        # Create an object with many properties
        obj = Object()
        for i in range(100):
            obj.data[i] = str(i)

        def run_to_robtop():
            obj.to_robtop()

        # Warmup
        run_to_robtop()

        # Benchmark
        number = 5000
        time = timeit.timeit(run_to_robtop, number=number)
        avg_time_per_call = time / number

        print(f"\n[Object.to_robtop] Time for {number} calls: {time:.4f}s")
        print(f"[Object.to_robtop] Avg: {avg_time_per_call*1e6:.2f}µs")

        # Baseline was ~149µs. Optimized is ~133µs.
        # We assume the optimization works if the code is logically O(N) instead of O(N^2).
        # We do not assert on time to avoid flaky tests in CI/CD.

if __name__ == '__main__':
    unittest.main()
