#!/usr/bin/env python3

# testAddingFunctions.py

import os
import time
import unittest

from rnglib import SimpleRNG


class SimpleClass():

    A = 42          # a python 'constant'

    def subtractor(self, x, y):
        return x - y

# Not an indentation error!  These functions are defined at the
# module level./x


def simpleAdder(self, a, b):
    return a + b


def add42(self, a):
    return a + self.A


class TestAddingFunctions (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def testAddingFuncs(self):
        """
        Demonstrate that functions can be added to instances dynamically
        and that 'self' within the added functions is interpreteed
        correctly.
        """

        obj = SimpleClass()
        x = self.rng.nextInt16()
        y = self.rng.nextInt16()
        q = self.rng.nextInt16()
        r = self.rng.nextInt16()

        # Test adding a function to an instance; this syntax is
        # specific to Python3.
        #           'object'           'instnace'  'owner'
        obj.adder = simpleAdder.__get__(SimpleClass, obj)
        self.assertEqual(obj.adder(x, y), x + y)

        # Confirm that 'self' is interpreted correctly in the added
        # functions.
        obj.plus42 = add42.__get__(SimpleClass, obj)
        self.assertEqual(obj.plus42(q), q + 42)

        # Newly added methods interacting with methods defined in the
        # class.
        self.assertEqual(
            obj.subtractor(obj.plus42(q), obj.adder(x, r)),
            (q + 42) - (x + r))


if __name__ == '__main__':
    unittest.main()
