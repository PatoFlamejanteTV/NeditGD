import unittest
import timeit
import os
from NeditGD.object_gd import Object

# Set dummy environment variable
os.environ["localappdata"] = "/tmp"

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_correctness(self):
        obj = Object(id=1, x=100, y=200)
        obj.groups = [1, 2, 3]

        # Property 31 is text, should be decoded as string
        obj[31] = "hello"

        # Property 1000 is unknown, encoded as text (base64), decoded as bytes by default fallthrough
        obj[1000] = "test"

        output = obj.to_robtop()

        # Check that it doesn't end with a comma
        self.assertFalse(output.endswith(','))

        # We can parse it back using from_robtop and compare equality
        obj_back = Object.from_robtop(output)

        self.assertEqual(obj_back[1], 1)
        self.assertEqual(obj_back['x'], 100)
        self.assertEqual(obj_back['y'], 200)
        self.assertEqual(obj_back['groups'], [1, 2, 3])

        self.assertEqual(obj_back[31], "hello")
        self.assertEqual(obj_back[1000], b"test")

    def test_to_robtop_performance(self):
        # Create an object with many properties
        obj = Object(id=1, x=100, y=200)
        for i in range(50):
            # Using int values to avoid base64 encoding overhead dominating the test,
            # but we want to test string concatenation overhead.
            # Using strings is fine as long as we compare apples to apples.
            obj[1000 + i] = f"property_value_{i}"

        obj.groups = list(range(10))

        def run_to_robtop():
            obj.to_robtop()

        # Warmup
        run_to_robtop()

        # Benchmark
        number = 10000
        time = timeit.timeit(run_to_robtop, number=number)
        avg_time_per_call = time / number

        print(f"\nTime for {number} calls: {time:.4f}s")
        print(f"Average time per call: {avg_time_per_call*1e6:.2f}µs")

if __name__ == '__main__':
    unittest.main()
