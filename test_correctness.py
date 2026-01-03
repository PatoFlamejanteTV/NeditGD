
import sys
import os
import unittest

# Set python path to current directory
sys.path.append(os.getcwd())

from NeditGD.object_gd import Object
import NeditGD.properties as properties

class TestPerformanceChanges(unittest.TestCase):
    def test_to_robtop_format(self):
        # Create an object with known properties
        obj = Object(id=1, x=30, y=15)
        # Default properties: 1:1, 2:30, 3:15, 155:1
        # Serialization order depends on dict iteration order (insertion order in Python 3.7+)
        # We can't guarantee order unless we sort, but we can check if it parses back correctly

        serialized = obj.to_robtop()
        print(f"Serialized: {serialized}")

        # Parse it back using from_robtop (which we didn't touch)
        obj2 = Object.from_robtop(serialized)

        self.assertEqual(obj[1], obj2[1])
        self.assertEqual(obj[2], obj2[2])
        self.assertEqual(obj[3], obj2[3])
        self.assertEqual(obj[155], obj2[155])

    def test_encode_text_redundancy(self):
        # Test that encode_text still produces correct base64url output
        text = "Hello World"
        encoded = properties.encode_text(31, text)
        # Expected: "31,<base64>,"
        parts = encoded.split(',')
        self.assertEqual(parts[0], '31')
        decoded_text = properties.decode_text(parts[1].encode())
        self.assertEqual(decoded_text, text)

        # Test with characters that change in base64url vs base64
        # Standard base64 uses + and /
        # URL safe uses - and _
        # We need input that produces + or /
        # "Subject?" -> U3ViamVjdD8= (standard)
        # "Subject?" -> U3ViamVjdD8= (url safe? wait, + is 62, / is 63)
        # 0xFB -> 11111011 -> ...

        # Let's just trust the python library implementation
        # But verify functionality is preserved
        text_special = "Hello? World!"
        encoded_special = properties.encode_text(31, text_special)
        parts_special = encoded_special.split(',')
        decoded_special = properties.decode_text(parts_special[1].encode())
        self.assertEqual(decoded_special, text_special)

if __name__ == '__main__':
    unittest.main()
