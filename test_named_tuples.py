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
        lower = two_pair(13, 'dddD')

        # create upper-level tuple
        threesome = namedtuple('Threesome', ['a__', 'b__', 'e__'])
        upper = threesome(a__='val0', b__=lower, e__=42)

        # attribute notation
        self.assertEqual(upper.a__, 'val0')
        self.assertEqual(upper.b__.c__, 13)
        self.assertEqual(upper.b__.d__, 'dddD')
        self.assertEqual(upper.e__, 42)

        # indexed access
        self.assertEqual(upper[0], 'val0')
        self.assertEqual(upper[1][0], 13)
        self.assertEqual(upper[1][1], 'dddD')
        self.assertEqual(upper[2], 42)

        # Immutability, attribute access.
        try:
            upper.a__ = 997
            self.fail("upper.a__ isn't immutable")        # pragma: no cover
        except AttributeError:
            self.assertEqual(upper.a__, 'val0')

        try:
            upper.b__ = 'happiness'
            self.fail("upper.b__ isn't immutable")        # pragma: no cover
        except AttributeError:
            # __eq__ works too
            self.assertEqual(upper.b__, lower)

        try:
            upper.b__.c__ = 'foo'
            self.fail("upper.b__.c__ isn't immutable")      # pragma: no cover
        except AttributeError:
            self.assertEqual(upper.b__.c__, 13)

        # Immutability, indexed assignment: we get a TypeError:
        #   "object does not support item assignment"
        try:
            upper[1][1] = 1942
            self.fail("upper[1][1] isn't immutable")    # pragma: no cover
        except TypeError:
            self.assertEqual(upper[1][1], 'dddD')

        try:
            upper[2] = 'baz'
            self.fail("upper[2] isn't immutable")       # pragma: no cover
        except TypeError:
            self.assertEqual(upper[2], 42)

if __name__ == '__main__':
    unittest.main()
