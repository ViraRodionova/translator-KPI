import unittest
from Main import translate
from Errors import *

class TestLab1(unittest.TestCase):
    def test_Test(self):
        filename = 'lab1/Test1'
        self.assertEqual(
            {
                'out': [401, 751, 59],
                'STRINGS': {751: 'LAB1'},
                'DIGITS': {},
                'positions': [
                    [1, 1], [1, 9], [1, 13]
                ]
            },
            translate(filename)
        )

    def test_TestLab1(self):
        filename = 'lab1/Test2'
        self.assertEqual(
            {
                'out': [401, 751, 59, 404, 501, 44, 502, 44, 503, 44, 504, 402, 505, 58, 405, 506, 59, 406, 752, 44, 505, 59, 407, 501, 59, 408, 504, 59, 753, 59, 403, 46],
                'STRINGS': {
                       751: 'TEST2',
                       752: 'MYVAR',
                       753: '234ABC'
                },
                'DIGITS': {
                    501: '4118',
                    502: '24',
                    503: '05',
                    504: '11',
                    505: '15',
                    506: '17'
                },
                'positions': [
                    [1, 1], [1, 9], [1, 14],
                    [5, 1], [5, 7], [5, 11],
                    [6, 9], [6, 11],
                    [7, 9], [7, 11],
                    [8, 9],
                    [10, 1],
                    [12, 5], [12, 7], [12, 8], [12, 13], [12, 15],
                    [13, 5], [13, 10], [13, 15], [13, 17], [13, 19],
                    [14, 5], [14, 8], [14, 12],
                    [15, 5], [15, 9], [15, 11],
                    [17, 5], [17, 11],
                    [19, 1], [19, 4]
                ]
            },
            translate(filename)
        )

    def test_unexpected_symbol(self):
        filename = 'lab1/Test3'
        self.assertRaises(
            UnexpectedSymbolException,
            translate, filename
        )

    def test_end_of_file(self):
        filename = 'lab1/Test4'
        self.assertRaises(
            EndOfFileException,
            translate, filename
        )

    def test_unexpected_symbol_2(self):
        filename = 'lab1/Test5'
        self.assertRaises(
            UnexpectedSymbolException,
            translate, filename
        )


if __name__ == '__main__':
    unittest.main()