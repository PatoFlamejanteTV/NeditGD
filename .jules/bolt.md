## 2024-05-23 - Property Decoding Optimization
**Learning:** Frequent dictionary and set lookups inside a tight loop (like parsing thousands of object properties) can significantly degrade performance. Moving constant lookups to module scope and using a dispatch table instead of multiple `if` checks provided a ~30-40% speedup.
**Action:** Always pre-calculate constant sets/dictionaries used in hot paths. Use dispatch tables for type-based logic where applicable.
