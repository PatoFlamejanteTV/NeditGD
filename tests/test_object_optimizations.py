import unittest
from NeditGD.object_gd import Object

class TestObjectOptimizations(unittest.TestCase):
    def test_to_robtop_correctness(self):
        obj = Object(id='spike', x=15, y=30)
        # Expected: id (1) = 8 (spike), x (2) = 15, y (3) = 30, 155 = 1 (default)
        # The order of keys depends on insertion order (Python 3.7+ guarantees it)
        # Default keys are inserted in __init__: 1:1, 2:0, 3:0, 155:1
        # Then kwargs update them.

        # Object(id='spike') -> sets key 1 to 8.
        # Object(x=15) -> sets key 2 to 15.
        # Object(y=30) -> sets key 3 to 30.

        # Keys in data:
        # 1: 8
        # 2: 15
        # 3: 30
        # 155: 1

        # properties.encode_property appends a comma.
        # to_robtop joins them and removes last char.

        rob = obj.to_robtop()

        # Since dictionary order is preserved, we expect:
        # "1,8,2,15,3,30,155,1"

        self.assertEqual(rob, "1,8,2,15,3,30,155,1")

    def test_to_robtop_with_tmp_keys(self):
        obj = Object(id='spike', _tmp_='ignore me')
        rob = obj.to_robtop()
        self.assertNotIn('ignore me', rob)
        self.assertIn('1,8', rob)

    def test_is_tmp_key(self):
        self.assertTrue(Object.is_tmp_key('_tmp_'))
        self.assertTrue(Object.is_tmp_key('_private_'))
        self.assertFalse(Object.is_tmp_key('normal'))
        self.assertFalse(Object.is_tmp_key('_start'))
        self.assertFalse(Object.is_tmp_key('end_'))
        self.assertFalse(Object.is_tmp_key('__')) # len is 2, not > 2

if __name__ == '__main__':
    unittest.main()
