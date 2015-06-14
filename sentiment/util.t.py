import unittest

import util

class TestCorpusReader(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_read_testdata(self):
        self.assertEqual("loovee", util.clean_word("loooooveeeeee"))


if __name__ == '__main__':
    unittest.main()
