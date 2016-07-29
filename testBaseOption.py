#!/usr/bin/env python3

# testBaseOption.py

import os
import time
import unittest

from rnglib import SimpleRNG
from optionz import _BaseOption, Option


class EmptyClass():
    pass


def simpleAdder(self, a, b):
    return a + b


class TestBaseOption (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def testConstructor(self):
        optA = Option(name='fred', surname='jones')
        # it's a dictionary
        self.assertTrue('name' in optA)
        self.assertTrue('surname'in optA)
        self.assertFalse('fred' in optA)
        # dots work
        self.assertEqual(optA.name, 'fred')
        self.assertEqual(optA.surname, 'jones')

        optB = Option(name='fred', surname='jones')
        self.assertEqual(optB.name, 'fred')
        self.assertEqual(optB.surname, 'jones')

        self.assertEqual(optA, optA)
        self.assertEqual(optA, optB)

        optC = Option(name='john', surname='smith')
        # dictionary
        self.assertTrue('name' in optC)
        self.assertTrue('surname' in optC)
        self.assertFalse('john' in optC)
        self.assertFalse('smith' in optC)
        # dots
        self.assertEqual(optC.name, 'john')
        self.assertEqual(optC.surname, 'smith')

        self.assertNotEqual(optA, optC)

        # assignment to dotted option
        optB.name = 'george'
        self.assertEqual(optB.name, 'george')

if __name__ == '__main__':
    unittest.main()
