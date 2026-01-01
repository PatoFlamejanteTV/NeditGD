## 2024-05-22 - Performance optimization in NeditGD
**Learning:** The 'NAME_TO_ID' dictionary in 'NeditGD/Dictionaries/PropertyID.py' is a large mapping. Repeated lookups in tight loops (like 'decode_property_pair' in 'NeditGD/properties.py') can be expensive. Pre-calculating sets of IDs or using direct integer comparisons where possible can improve performance.
**Action:** Move set constructions out of hot paths and into module-level constants.
