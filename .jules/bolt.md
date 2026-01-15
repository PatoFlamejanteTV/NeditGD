## 2024-05-23 - Dictionary Lookup Performance
**Learning:** Python dictionary iteration (`.items()`) for reverse lookup is significantly slower than O(1) direct lookup, especially in hot paths like property name resolution.
**Action:** Always maintain a reverse mapping dictionary (e.g., `ID_TO_NAME`) when frequent bidirectional lookups are required. Pre-calculate constant sets/dictionaries at module level instead of recreating them in function calls.

## 2026-01-15 - Module-level Execution and Testing
**Learning:** Importing the top-level `NeditGD` package triggers module-level execution in `saveload.py` that relies on `os.getenv('localappdata')`. This makes unit testing individual components (like `Object`) difficult without mocking environment variables or using selective imports.
**Action:** Mock `localappdata` in test setup or use direct sub-module imports (e.g., `from NeditGD.object_gd import Object`) to bypass the top-level package initialization when possible.
