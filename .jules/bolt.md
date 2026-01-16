## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.
## 2024-05-24 - String Construction and Type Checking Overhead
**Learning:** In extremely hot loops (100k+ iterations), standard string concatenation (`+=`) is a major bottleneck compared to `list.append` + `''.join`. Additionally, strict type checking (`type(x) is T`) can be faster than `isinstance(x, T)` and useful for avoiding subclass behavior (e.g., `bool` inheriting from `int`) when encoding data where format matters.
**Action:** Use list accumulation for large string builds. Consider inline strict type checks to bypass function call overhead for high-frequency primitive types.
