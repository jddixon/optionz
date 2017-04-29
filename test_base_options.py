#!/usr/bin/env python3
# testBaseOption.py

"""  Test the Option class. """

import time
import unittest

from rnglib import SimpleRNG
from optionz import Option

# pylint: disable=too-few-public-methods


class EmptyClass():
    """ Stub class, for testing. """
    pass


# pylint: disable=unused-argument
def simple_adder(self, a__, b__):
    """ Simplest possible adder method. """
    return a__ + b__


class TestBaseOption(unittest.TestCase):
    """ Test the [Base]Option class. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_constructor(self):
        """ Test the constuctor. """

        opt_a = Option(name='fred', surname='jones')
        # it's a dictionary
        self.assertTrue('name' in opt_a)
        self.assertTrue('surname'in opt_a)
        self.assertFalse('fred' in opt_a)
        # dots work
        self.assertEqual(opt_a.name, 'fred')
        # pylint: disable=no-member
        self.assertEqual(opt_a.surname, 'jones')

        opt_b = Option(name='fred', surname='jones')
        self.assertEqual(opt_b.name, 'fred')
        # pylint: disable=no-member
        self.assertEqual(opt_b.surname, 'jones')

        self.assertEqual(opt_a, opt_a)
        self.assertEqual(opt_a, opt_b)

        opt_c = Option(name='john', surname='smith')
        # dictionary
        self.assertTrue('name' in opt_c)
        self.assertTrue('surname' in opt_c)
        self.assertFalse('john' in opt_c)
        self.assertFalse('smith' in opt_c)
        # dots
        self.assertEqual(opt_c.name, 'john')
        # pylint: disable=no-member
        self.assertEqual(opt_c.surname, 'smith')

        self.assertNotEqual(opt_a, opt_c)

        # assignment to dotted option
        opt_b.name = 'george'
        self.assertEqual(opt_b.name, 'george')


if __name__ == '__main__':
    unittest.main()
