# test_sap.py

import unittest
import sap.pipeline as pipeline

class TestModule(unittest.TestCase):
    def test_test(self):
        print(pipeline.main)
        pass

if __name__ == '__main__':
    unittest.main()