import sys
import os
import timeit

# Ensure we can import NeditGD
sys.path.append(os.getcwd())

from NeditGD.object_gd import Object

def benchmark_to_robtop():
    # Create an object with many properties to simulate a complex object
    # We use a mix of int keys and aliases if possible, but mainly int keys are stored internally
    obj = Object(id=1, x=100, y=200)

    # Add a reasonable number of properties.
    # Real objects might have 10-50 properties.
    for i in range(50):
        obj[i + 1000] = f"val{i}"

    def run_to_robtop():
        return obj.to_robtop()

    # Verify correctness first
    res = run_to_robtop()
    assert isinstance(res, str)
    assert len(res) > 0

    number = 10000
    time = timeit.timeit(run_to_robtop, number=number)
    print(f"Time for {number} calls: {time:.4f}s")
    print(f"Average time per call: {time / number * 1e6:.2f}µs")

if __name__ == "__main__":
    benchmark_to_robtop()
