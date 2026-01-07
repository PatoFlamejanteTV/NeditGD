import unittest
import timeit
import base64
from NeditGD.properties import encode_text

class TestPerformance(unittest.TestCase):
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
        print(f"\nTime for {number} calls: {time:.4f}s")
        print(f"Average time per call: {time/number*1e6:.2f}µs")

    def test_encode_text_correctness(self):
        text = "Hello World"
        p_id = 31
        encoded = encode_text(p_id, text)

        # Expected encoding
        # text.encode() -> b'Hello World'
        # base64.b64encode(..., altchars=b'-_') -> b'SGVsbG8gV29ybGQ='
        expected_b64 = base64.b64encode(text.encode(), altchars=b'-_').decode()
        expected = f'{p_id},{expected_b64},'

        self.assertEqual(encoded, expected)

if __name__ == '__main__':
    unittest.main()
