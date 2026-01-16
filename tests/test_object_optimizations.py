import unittest
import timeit
import os

# Set env var before import
os.environ['localappdata'] = '/tmp'

from NeditGD.object_gd import Object

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_performance(self):
        # Create an object with many properties
        obj = Object(id=1, x=10.5, y=20.5, rotation=45)
        for i in range(100):
            obj[1000 + i] = i
        obj.text = "Hello World"
        obj._tmp_key_ = "should be ignored"

        def run_to_robtop():
            obj.to_robtop()

        # Warmup
        run_to_robtop()

        number = 5000
        time = timeit.timeit(run_to_robtop, number=number)
        avg_time_per_call = time / number

        print(f"\n[Object.to_robtop] Time for {number} calls: {time:.4f}s")
        print(f"[Object.to_robtop] Average time per call: {avg_time_per_call*1e6:.2f}µs")

        # Basic regression check (loose bound)
        self.assertLess(avg_time_per_call, 0.000200, "Performance regression: to_robtop is too slow")

    def test_to_robtop_correctness(self):
        obj = Object(id=1, x=10, y=20)
        obj.text = "Test" # Property 31
        obj._tmp = "ignore"

        # Expected encoding (order depends on dict insertion order, but UserDict usually preserves it)
        # properties: 1 (id), 2 (x), 3 (y), 155 (default 1)
        # We initialized with id=1, x=10, y=20.
        # Defaults are set in __init__: {1:1, 2:0, 3:0, 155:1}
        # Overwritten by kwargs.

        # Actually Object.__init__ calls super().__init__ which sets defaults, then updates with kwargs.
        # Python 3.7+ preserves insertion order.
        # Defaults: 1, 2, 3, 155.
        # Then kwargs: id=1 (update 1), x=10 (update 2), y=20 (update 3).
        # Then text (31).

        # So keys should be 1, 2, 3, 155, 31.

        res = obj.to_robtop()

        # We verify segments exist because order might vary if implementation changes (though standard dict shouldn't)
        self.assertIn("1,1", res)
        self.assertIn("2,10", res)
        self.assertIn("3,20", res)
        self.assertIn("155,1", res)
        # text is base64 encoded. 'Test' -> 'VGVzdA=='
        self.assertIn("31,VGVzdA==", res)

        # Check that it does not end with comma
        self.assertFalse(res.endswith(','))

        # Check that ignored key is not present
        self.assertNotIn("ignore", res)

if __name__ == '__main__':
    unittest.main()
