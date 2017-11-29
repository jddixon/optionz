#!/usr/bin/env python3
# testNamedTuples.py

""" Test named tuples. """

import unittest

from collections import namedtuple


class TestNamedTuples(unittest.TestCase):
    """ Test behavior of named tuples. """

    def test_functionality(self):
        """
        Nested named tuples work more or less as expected.  Lower-level
        tuples must be built first, because the tuples are immutable.
        """

        # creation of lower-level tuple
        two_pair = namedtuple('TwoPair', ['c__', 'd__'])
        duo = two_pair(13, 'dddD')

        # create upper-level tuple
        threesome = namedtuple('Threesome', ['a__', 'b__', 'e__'])
        trio = threesome(a__='val0', b__=duo, e__=42)

        # attribute notation
        self.assertEqual(trio.a__, 'val0')
        self.assertEqual(trio.b__.c__, 13)
        self.assertEqual(trio.b__.d__, 'dddD')
        self.assertEqual(trio.e__, 42)

        # indexed access
        self.assertEqual(trio[0], 'val0')
        self.assertEqual(trio[1][0], 13)
        self.assertEqual(trio[1][1], 'dddD')
        self.assertEqual(trio[2], 42)

        # Immutability, attribute access.
        try:
            trio.a__ = 997
            self.fail("trio.a__ isn't immutable")        # pragma: no cover
        except AttributeError:
            self.assertEqual(trio.a__, 'val0')

        try:
            trio.b__ = 'happiness'
            self.fail("trio.b__ isn't immutable")        # pragma: no cover
        except AttributeError:
            # __eq__ works too
            self.assertEqual(trio.b__, duo)

        try:
            trio.b__.c__ = 'foo'
            self.fail("trio.b__.c__ isn't immutable")      # pragma: no cover
        except AttributeError:
            self.assertEqual(trio.b__.c__, 13)

        # Immutability, indexed assignment: we get a TypeError:
        #   "object does not support item assignment"
        try:
            trio[1][1] = 1942
            self.fail("trio[1][1] isn't immutable")    # pragma: no cover
        except TypeError:
            self.assertEqual(trio[1][1], 'dddD')

        try:
            # pylint: disable=unsupported-assignment-operation
            trio[2] = 'baz'
            self.fail("trio[2] isn't immutable")       # pragma: no cover
        except TypeError:
            self.assertEqual(trio[2], 42)


if __name__ == '__main__':
    unittest.main()
