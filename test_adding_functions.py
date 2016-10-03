#!/usr/bin/env python3
# test_adding_functions.py

""" Test adding functions to a class dynamically.  """

import time
import unittest

from rnglib import SimpleRNG


class SimpleClass():
    """ Simple class for testing constancy. """

    A42 = 42          # a python 'constant'

    def subtractor(self, x_val, y_val):
        """ Toy function for testing. """
        return x_val - y_val

# Not an indentation error!  These functions are defined at the
# module level.


def simple_adder(self, a_val, b_val):
    """ Simplest possible adder method. """
    return a_val + b_val


def add42(self, a_val):
    """ Add a class constant to a variable. """
    return a_val + self.A42


class TestAddingFunctions(unittest.TestCase):
    """ Test adding functions to an existing class. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_adding_funcs(self):
        """
        Demonstrate that functions can be added to instances dynamically
        and that 'self' within the added functions is interpreteed
        correctly.
        """

        obj = SimpleClass()
        x_val = self.rng.nextInt16()
        y_val = self.rng.nextInt16()
        q_val = self.rng.nextInt16()
        r_val = self.rng.nextInt16()

        # Test adding a function to an instance; this syntax is
        # specific to Python3.
        #           'object'           'instnace'  'owner'
        obj.adder = simple_adder.__get__(SimpleClass, obj)
        self.assertEqual(obj.adder(x_val, y_val), x_val + y_val)

        # Confirm that 'self' is interpreted correctly in the added
        # functions.
        obj.plus42 = add42.__get__(SimpleClass, obj)
        self.assertEqual(obj.plus42(q_val), q_val + 42)

        # Newly added methods interacting with methods defined in the
        # class.
        self.assertEqual(
            obj.subtractor(obj.plus42(q_val), obj.adder(x_val, r_val)),
            (q_val + 42) - (x_val + r_val))


if __name__ == '__main__':
    unittest.main()
