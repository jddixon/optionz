#!/usr/bin/env python3
# testBaseOption.py

"""  Test the dump_options_ method. """

import unittest

from argparse import Namespace
from optionz import dump_options

JUST_HEADERS = 'OPTION VALUE\n'

# pylint: disable=too-few-public-methods


class TestDumpOptions(unittest.TestCase):
    """  Test the dump_options_ method. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_options(self):
        """ Test behavior of empty set of options. """

        ns_ = None
        self.assertEqual(dump_options(None, with_headers=False), '')
        self.assertEqual(dump_options(None, with_headers=True), JUST_HEADERS)
        self.assertEqual(dump_options(None), JUST_HEADERS)

        ns_ = Namespace()
        self.assertEqual(dump_options(None, with_headers=False), '')
        self.assertEqual(dump_options(None, with_headers=True), JUST_HEADERS)
        self.assertEqual(dump_options(None), JUST_HEADERS)

    def test_simple_options(self):
        """ Test behavior where all option values are scalars. """

        # all strings, single character keys ------------------------

        kwargs = {'z': 'zulu', 'x': 'xray', 'a': 'alpha', 'f': 'foxtrot'}
        expected = """a alpha
f foxtrot
x xray
z zulu
"""
        ns_ = Namespace(**kwargs)
        self.assertEqual(dump_options(ns_, with_headers=False), expected)

        # all strings, varying-length string keys -------------------

        kwargs = {'z': 'zulu', 'xyz': 'xray', 'ab': 'alpha', 'fghi': 'foxtrot'}
        expected = """ab   alpha
fghi foxtrot
xyz  xray
z    zulu
"""
        ns_ = Namespace(**kwargs)
        self.assertEqual(dump_options(ns_, with_headers=False), expected)

        # varying-length string keys, various types of values -------

        kwargs = {'z': False, 'xyz': 97, 'ab': 45.2, 'fghi': 'foxtrot'}
        expected = """ab   45.200000
fghi foxtrot
xyz  97
z    False
"""
        ns_ = Namespace(**kwargs)
        self.assertEqual(dump_options(ns_, with_headers=False), expected)

    def test_wider_option_names(self):
        """ Test behavior with wider options names. """

        # all strings, varying-length string keys -------------------

        kwargs = {'z': 'zulu', 'xyz': 'xray', 'ab12345': 'alpha',
                  'fghi': 'foxtrot'}
        expected = """ab12345 alpha
fghi    foxtrot
xyz     xray
z       zulu
"""
        ns_ = Namespace(**kwargs)
        self.assertEqual(dump_options(ns_, with_headers=False), expected)

    def test_with_list_options(self):
        """ Test behavior where some option values are lists. """

        # single list, various types of values ----------------------

        kwargs = {'z': False, 'xyz': 995, 'ab': 45.2, 'fghi': 'foxtrot',
                  'baz': ['a', 995, True]}
        expected4 = """ab   45.200000
fghi foxtrot
xyz  995
z    False

BAZS:
    a
    995
    True
"""
        ns_ = Namespace(**kwargs)
        self.assertEqual(dump_options(ns_, with_headers=False), expected4)

        # same setup, but with headers ------------------------------
        # notice that pluralizing 'baz' to 'bazs' makes no sense
        # notice also that indent on list values is fixed

        expected6 = """ab     45.200000
fghi   foxtrot
xyz    995
z      False

BAZS:
    a
    995
    True
"""
        self.assertEqual(dump_options(ns_, with_headers=True),
                         JUST_HEADERS + expected6)


if __name__ == '__main__':
    unittest.main()
