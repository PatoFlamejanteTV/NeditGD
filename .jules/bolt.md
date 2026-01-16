## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.

## 2024-05-24 - Serialization Hot Path Optimization
**Learning:** String concatenation (`+=`) in serialization loops is a major bottleneck (O(N^2)). Switching to list accumulation (`join`) provided a ~2x speedup. Inlining common type checks (`int`/`float`) to bypass generic encoder functions further reduces call overhead in tight loops.
**Action:** Use list accumulation for all serialization logic. Inline type checks for primitive types in hot paths where function call overhead is comparable to the operation cost.
