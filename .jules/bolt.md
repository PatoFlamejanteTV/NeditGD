## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.

## 2024-05-24 - String Accumulation in Serialization
**Learning:** In `NeditGD`, the `encode_property` functions append a trailing comma, requiring the consumer to slice the result (`[:-1]`). While `"".join()` is faster than `+=`, the improvement is dampened by the overhead of creating many small intermediate strings in `encode_property`.
**Action:** When optimizing serialization, prefer `list` accumulation and `"".join()` over string concatenation. For deeper optimization, consider refactoring inner functions to yield components rather than constructing partial strings.
