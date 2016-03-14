#!/usr/bin/python3

# testOptionz.py

import os, time, unittest

from rnglib         import SimpleRNG
from optionz_py     import *

class TestOptionz (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG( time.time() )
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
    
    def testBareOptionz (self):
        optionz = Optionz('fred')
        self.assertEqual(optionz.name,         'fred')
        self.assertEqual(optionz.description,   None)
        self.assertEqual(optionz.epilog,        None)
        self.assertEqual(len(optionz),          0)

        optionz = Optionz('frank', 'frivolous', 'fabulous')
        self.assertEqual(optionz.name,         'frank')
        self.assertEqual(optionz.description,   'frivolous')
        self.assertEqual(optionz.epilog,        'fabulous')
        self.assertEqual(len(optionz),          0)

    def testZOptions(self):
        boolOpt     = BoolOption('bO', default=True, description="I'm small")
        self.assertEqual(boolOpt.name, 'bO')
        self.assertEqual(boolOpt.default, True)
        self.assertEqual(boolOpt.description, "I'm small")


if __name__ == '__main__':
    unittest.main()
