## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.
## 2024-05-24 - String Concatenation vs List Accumulation
**Learning:** In a hot serialization loop (`Object.to_robtop`), replacing string concatenation (`+=`) with list accumulation (`[].append` + `''.join`) provided a ~14% speedup. Caching global/class method lookups (`properties.encode_property`, `Object.is_tmp_key`) to local variables further reduced overhead.
**Action:** Use list accumulation for constructing large strings in loops. Cache global functions/methods in local variables for tight loops.
