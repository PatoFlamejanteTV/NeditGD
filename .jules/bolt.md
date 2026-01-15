## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.

## 2026-01-15 - String Concatenation in Serialization
**Learning:** `Object.to_robtop` used string concatenation in a loop, which is O(N^2). Since objects can have many properties and there are thousands of objects, this is a significant bottleneck.
**Action:** Use list accumulation (`[].append`) and `''.join()` for all serialization methods. Cache global lookups in local variables for tight loops.
