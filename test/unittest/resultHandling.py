import unittest
import os, sys
import json
import logging
testdir = os.path.dirname(__file__)
srcdir = '../../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from function import convertToDict



class resultHandling(unittest.TestCase):
    def test_convertToDict(self):
        d = {'field1': 'example', 'filed2': 4.5}
        s = json.dumps(d)
        d_ = convertToDict(s)
        self.assertEqual(d, d_)

if __name__ == "__main__":
    unittest.main()
