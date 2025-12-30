# Bolt's Journal

## 2025-02-19 - Object deserialization inefficiency
**Learning:** `NeditGD`'s `Object.from_robtop` creates intermediate dictionaries and uses `__init__` which triggers expensive property parsing/dispatching for every object. Bypassing this by directly populating `self.data` with integer keys yields significant (~40%) performance gains.
**Action:** When optimizing data classes wrapping `UserDict` or similar, look for overhead in `__setitem__` or `__getattr__` and consider direct data access for bulk operations like loading.
