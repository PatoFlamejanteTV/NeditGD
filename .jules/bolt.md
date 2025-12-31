## 2024-05-23 - [Set Construction Overhead]
**Learning:** Constructing sets or lists inside a hot function (like `decode_property_pair`) happens on *every call*. For high-frequency functions (parsing 100k+ objects), this overhead is significant.
**Action:** Move constant sets/lists to module-level constants so they are created only once at import time.
