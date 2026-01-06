
import sys
import os
import unittest
import base64
import tempfile
import shutil

sys.path.append(os.getcwd())

# Setup localappdata with a temp directory
temp_dir = tempfile.mkdtemp()
os.environ['localappdata'] = temp_dir

from NeditGD.object_gd import Object
import NeditGD.properties as properties
from NeditGD.Dictionaries.PropertyID import NAME_TO_ID

class TestOptimizations(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        # Cleanup temp directory
        shutil.rmtree(temp_dir)

    def test_encode_text(self):
        text = "Hello World"
        p_id = NAME_TO_ID.get('text', 31) # Dynamic lookup with fallback
        encoded = properties.encode_text(p_id, text)

        # Verify format: p_id,base64,
        parts = encoded.split(',')
        self.assertEqual(len(parts), 3) # "31,base64," splits to ["31", "base64", ""]
        self.assertEqual(parts[0], str(p_id))
        self.assertEqual(parts[2], '')

        # Verify content
        encoded_content = parts[1]
        decoded = base64.b64decode(encoded_content, altchars=b'-_').decode()
        self.assertEqual(decoded, text)

    def test_to_robtop(self):
        obj = Object(id=1, x=10, y=20)
        # Add some properties that use text encoding
        obj.text = "Test Text"

        robtop_str = obj.to_robtop()

        # Basic checks
        self.assertIn("1,1,", robtop_str)
        self.assertIn("2,10,", robtop_str)
        self.assertIn("3,20,", robtop_str)

        # Verify reconstruction
        obj2 = Object.from_robtop(robtop_str)
        self.assertEqual(obj2[1], 1)
        self.assertEqual(obj2['x'], 10)
        self.assertEqual(obj2['y'], 20)

        # We need to find the text property ID.
        text_id = NAME_TO_ID['text']

        self.assertEqual(obj2[text_id], "Test Text")

if __name__ == '__main__':
    unittest.main()
