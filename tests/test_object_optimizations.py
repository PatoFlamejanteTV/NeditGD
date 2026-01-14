import unittest
import os
import sys

# Ensure NeditGD is importable
sys.path.append(os.getcwd())

from NeditGD.object_gd import Object

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_correctness(self):
        # Create an object with known properties
        # ID 1 is 'id', ID 2 is 'x', ID 3 is 'y'
        obj = Object(id=1, x=30, y=60)
        # 1,1,2,30,3,60,155,1
        # Order might vary depending on dict iteration, but usually insertion order for recent Python
        # Object init sets 1:1, 2:0, 3:0, 155:1 first.
        # Then kwargs overwrite.

        # Let's inspect the output
        encoded = obj.to_robtop()

        # Check that all properties are present
        self.assertIn("1,1", encoded)
        self.assertIn("2,30", encoded)
        self.assertIn("3,60", encoded)
        self.assertIn("155,1", encoded) # Default property

        # Ensure format is correct (comma separated pairs)
        parts = encoded.split(',')
        self.assertEqual(len(parts) % 2, 0)

        # Test with list property
        obj.groups = [10, 20] # group ID is 57
        encoded = obj.to_robtop()
        self.assertIn("57,10.20", encoded)

        # Test with tmp key (should be ignored)
        obj._tmp__ = "ignore me"
        encoded = obj.to_robtop()
        self.assertNotIn("ignore me", encoded)

        # Test with text
        obj.text = "Hello" # ID 31
        encoded = obj.to_robtop()
        # 31,SGVsbG8=
        self.assertIn("31,SGVsbG8=", encoded)

if __name__ == '__main__':
    unittest.main()
