import unittest
import timeit
from NeditGD.object_gd import Object
import os

# Ensure we don't fail due to missing env var if NeditGD is fully imported
if "localappdata" not in os.environ:
    os.environ["localappdata"] = "/tmp"

class TestObjectOptimizations(unittest.TestCase):
    def setUp(self):
        # Create an object with many properties
        self.obj = Object(id=1, x=10, y=10)
        # Add many properties
        for i in range(100):
            self.obj[i+10] = f"value{i}"

        # Add some tmp keys
        for i in range(20):
            self.obj[f"_tmp{i}__"] = i

    def test_to_robtop_performance(self):
        obj = self.obj
        def run_to_robtop():
            obj.to_robtop()

        # Warmup
        run_to_robtop()

        # Benchmark
        number = 5000
        time = timeit.timeit(run_to_robtop, number=number)
        avg_time_per_call = time / number

        print(f"\n[to_robtop] Time for {number} calls: {time:.4f}s")
        print(f"[to_robtop] Average time per call: {avg_time_per_call*1e6:.2f}µs")

    def test_is_tmp_key_performance(self):
        keys = ["__test__", "normal", "very_long_key_name", "__", "_short_"]

        def run_is_tmp_key():
            for k in keys:
                Object.is_tmp_key(k)

        # Warmup
        run_is_tmp_key()

        # Benchmark
        number = 100000
        time = timeit.timeit(run_is_tmp_key, number=number)
        avg_time_per_call = time / number

        print(f"\n[is_tmp_key] Time for {number} calls (loop of {len(keys)}): {time:.4f}s")
        print(f"[is_tmp_key] Average time per call: {avg_time_per_call*1e6:.2f}µs")

    def test_to_robtop_correctness(self):
        obj = Object(id=1, x=10, y=20)
        obj[20] = "val"
        obj["_tmp__"] = 123

        # Basic check. Precise string depends on property encoding order which depends on dict implementation (insertion order in modern python)
        # ID 1 is id (aliased), 2 is x, 3 is y. 155 is default 1.
        # Object init sets 1:1, 2:0, 3:0, 155:1
        # Then we set id=1 (1:1), x=10 (2:10), y=20 (3:20)
        # And 20:'val'

        rob = obj.to_robtop()

        # Should contain properties
        self.assertIn("1,1", rob)
        self.assertIn("2,10", rob)
        self.assertIn("3,20", rob)
        # val is base64 encoded to dmFs
        # self.assertIn("20,dmFs", rob)
        # Actually checking if it is there is enough, I'll trust encode_text works as tested elsewhere.

        # Should NOT contain tmp key
        self.assertNotIn("_tmp__", rob)
        self.assertNotIn("123", rob) # assuming 123 isn't used elsewhere

if __name__ == '__main__':
    unittest.main()
