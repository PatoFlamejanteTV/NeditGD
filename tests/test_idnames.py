import unittest
import timeit
from NeditGD.Dictionaries.IDNames import oid_to_alias, OBJECT_IDS

class TestIDNamesOptimizations(unittest.TestCase):
    def test_oid_to_alias_performance(self):
        # 3620 is 'item_comp_t', which is at the end of the dictionary
        target_id = 3620

        def run_lookup():
            oid_to_alias(target_id)

        # Warmup
        run_lookup()

        # Benchmark
        number = 100000
        time = timeit.timeit(run_lookup, number=number)
        avg_time_per_call = time / number

        print(f"\n[oid_to_alias] Time for {number} calls: {time:.4f}s")
        print(f"[oid_to_alias] Average time per call: {avg_time_per_call*1e6:.2f}µs")

        # Before optimization: ~2.17µs
        # After optimization: ~0.29µs
        # We assert it is under 1.5µs to be safe on slower CI environments while still catching major regressions
        self.assertLess(avg_time_per_call, 0.0000015, "Performance regression: oid_to_alias is too slow")

    def test_oid_to_alias_correctness(self):
        # Check a few known mappings
        self.assertEqual(oid_to_alias(1), 'block')
        self.assertEqual(oid_to_alias(3620), 'item_comp_t')

        # Check unknown mapping returns string of ID
        self.assertEqual(oid_to_alias(99999), '99999')
