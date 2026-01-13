
import unittest
from NeditGD.object_gd import Object

class TestObjectToRobtop(unittest.TestCase):
    def test_to_robtop_format(self):
        """Test that to_robtop produces correctly formatted string."""
        obj = Object(x=10, y=20, groups=[1, 2])
        # Expected components (order may vary but key-value pairs must exist)
        # Default keys: 1(id):1, 2(x):0->10, 3(y):0->20, 155:1
        # groups(57):[1,2] -> "1.2"

        s = obj.to_robtop()
        self.assertIsInstance(s, str)
        self.assertTrue(len(s) > 0)
        self.assertFalse(s.endswith(','))

        parts = s.split(',')
        self.assertEqual(len(parts) % 2, 0, "String should contain pairs of key,value")

        # Convert to dict for verification
        data = {}
        for i in range(0, len(parts), 2):
            data[int(parts[i])] = parts[i+1]

        self.assertEqual(data[1], '1')
        self.assertEqual(data[2], '10')
        self.assertEqual(data[3], '20')
        self.assertEqual(data[155], '1')
        self.assertEqual(data[57], '1.2')

    def test_empty_robtop(self):
        """Test validation on a default object."""
        obj = Object()
        s = obj.to_robtop()
        self.assertTrue(len(s) > 0)
        self.assertFalse(s.endswith(','))

if __name__ == '__main__':
    unittest.main()
