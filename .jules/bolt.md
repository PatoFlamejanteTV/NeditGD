## 2024-05-23 - String Concatenation Bottleneck
**Learning:** Python's string concatenation in loops (`+=`) creates a new string object each iteration, leading to $O(N^2)$ complexity. Using `list.append` and `"".join()` reduces this to $O(N)$.
**Action:** Always verify string construction methods in tight loops, especially for serialization/encoding tasks.
