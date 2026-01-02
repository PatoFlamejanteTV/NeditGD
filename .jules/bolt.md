## 2024-05-23 - String Concatenation in Loops
**Learning:** Python's string concatenation (`+=`) in loops is an O(N²) operation because strings are immutable, leading to frequent memory reallocations. Using `list.append()` and `"".join()` reduces this to O(N).
**Action:** Always prefer `"".join()` for constructing strings from multiple parts, especially inside loops or when the number of parts is large.
