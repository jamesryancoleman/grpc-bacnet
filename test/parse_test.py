import unittest
from src.parse import ParseBacnetPtKey

class ParseTest(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test/sample_xrefs"
        self.test_keys = []
        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]

    def test_key_access(self):
        for k in self.test_keys:
            print(k)
    
    def test_parse_key(self):
        for k in self.test_keys:
            params = ParseBacnetPtKey(k)
            print(repr(params))
            