#!/usr/bin/env python3

# testNamedTuples.py

import os
import time
import unittest

from collections import namedtuple


class TestNamedTuples (unittest.TestCase):

    def testFunctionality(self):
        """
        Nested named tuples work more or less as expected.  Lower-level
        tuples must be built first, because the tuples are immutable.
        """

        # creation of lower-level tuple
        TwoPair = namedtuple('TwoPair', ['c', 'd'])
        lower = TwoPair(13, 'dddD')

        # create upper-level tuple
        Threesome = namedtuple('Threesome', ['a', 'b', 'e'])
        upper = Threesome(a='val0', b=lower, e=42)

        # attribute notation
        self.assertEqual(upper.a, 'val0')
        self.assertEqual(upper.b.c, 13)
        self.assertEqual(upper.b.d, 'dddD')
        self.assertEqual(upper.e, 42)

        # indexed access
        self.assertEqual(upper[0], 'val0')
        self.assertEqual(upper[1][0], 13)
        self.assertEqual(upper[1][1], 'dddD')
        self.assertEqual(upper[2], 42)

        # Immutability, attribute access.
        try:
            upper.a = 997
            self.fail("upper.a isn't immutable")        # pragma: no cover
        except AttributeError:
            self.assertEqual(upper.a, 'val0')

        try:
            upper.b = 'happiness'
            self.fail("upper.b isn't immutable")        # pragma: no cover
        except AttributeError:
            # __eq__ works too
            self.assertEqual(upper.b, lower)

        try:
            upper.b.c = 'foo'
            self.fail("upper.b.c isn't immutable")      # pragma: no cover
        except AttributeError:
            self.assertEqual(upper.b.c, 13)

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
