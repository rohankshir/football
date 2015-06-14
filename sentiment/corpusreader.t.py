import unittest

import corpusreader

class TestCorpusReader(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_read_testdata(self):
        test_data = corpusreader.get_test_data()
        self.assertEqual(test_data[0][1], 4)
        self.assertEqual(test_data[0][0][0],"@stellargirl")
        self.assertEqual(test_data[0][0][1],"I")

if __name__ == '__main__':
    unittest.main()
