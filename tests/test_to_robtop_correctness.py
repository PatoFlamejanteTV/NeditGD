
import unittest
import sys
import os

sys.path.append(os.getcwd())

from NeditGD.object_gd import Object

class TestToRobTop(unittest.TestCase):
    def test_simple_types(self):
        obj = Object(id=1, x=10, y=20)
        # Assuming id=1, x=2, y=3, 155=155 are the IDs
        # Default keys: 1:1, 2:0, 3:0, 155:1
        # Modified: 1:1, 2:10, 3:20, 155:1

        # Check generated string format
        s = obj.to_robtop()
        # The order of keys is not guaranteed in python < 3.7 but we assume python 3.7+ (ordered dicts)
        # However, checking containment is safer. We check k,v pairs.

        # We expect pairs like "1,1", "2,10", "3,20", "155,1"
        # And they are separated by commas.
        # Since the order matters for reconstructing the string exactly, we just check if the pairs exist in the split list.
        parts = s.split(',')
        # Convert list to dict for verification
        d = {}
        for i in range(0, len(parts), 2):
            d[int(parts[i])] = parts[i+1]

        self.assertEqual(d[1], '1')
        self.assertEqual(d[2], '10')
        self.assertEqual(d[3], '20')
        self.assertEqual(d[155], '1')

    def test_list_type(self):
        obj = Object(id=1, groups=[10, 20])
        s = obj.to_robtop()
        # groups ID is 57
        # We check if 57 exists and value is 10.20
        parts = s.split(',')
        d = {}
        for i in range(0, len(parts), 2):
            d[int(parts[i])] = parts[i+1]

        self.assertEqual(d[57], '10.20')

    def test_float_type(self):
        obj = Object(id=1, x=10.5)
        s = obj.to_robtop()
        parts = s.split(',')
        d = {}
        for i in range(0, len(parts), 2):
            d[int(parts[i])] = parts[i+1]
        self.assertEqual(d[2], '10.5')

if __name__ == '__main__':
    unittest.main()
