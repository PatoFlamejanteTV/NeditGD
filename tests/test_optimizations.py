import unittest
import timeit
import base64
from NeditGD.properties import encode_text

class TestEncodeTextOptimizations(unittest.TestCase):
    def test_encode_text_performance(self):
        text = "Hello World! " * 100
        p_id = 31

        def run_encode():
            encode_text(p_id, text)

        # Warmup
        run_encode()

        # Benchmark
        number = 10000
        time = timeit.timeit(run_encode, number=number)
        avg_time_per_call = time / number

        print(f"\nTime for {number} calls: {time:.4f}s")
        print(f"Average time per call: {avg_time_per_call*1e6:.2f}µs")

        # Assert performance is within reasonable bounds (e.g. < 20µs on this environment)
        # Baseline was ~10-12µs before optimization, ~6µs after.
        # We set a conservative upper bound to avoid flaky tests on slower CI runners.
        self.assertLess(avg_time_per_call, 0.000020, "Performance regression detected: encode_text is too slow")

    def test_encode_text_correctness(self):
        text = "Hello World"
        p_id = 31
        encoded = encode_text(p_id, text)

        # Expected: "Hello World" base64-encoded with URL-safe altchars
        # 'Hello World' -> b'SGVsbG8gV29ybGQ='
        expected = '31,SGVsbG8gV29ybGQ=,'

        self.assertEqual(encoded, expected)

if __name__ == '__main__':
    unittest.main()
