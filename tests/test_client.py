import unittest
import pyfldigi


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = pyfldigi.Client()

    def test_name(self):
        self.assertEqual(self.client.name, 'fldigi')


if __name__ == '__main__':
    unittest.main()
