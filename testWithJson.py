#!/usr/bin/env python3

# testWithJson.py

import io
import json
import os
import time
import unittest

from rnglib import SimpleRNG
from optionz import (Optionz,
                     BoolOption, ChoiceOption,
                     FloatOption, IntOption, ListOption, StrOption)


class TestWithJson (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def testBoolOptions(self):

        o1 = BoolOption('eeenie')
        self.assertEqual(o1.name, 'eeenie')
        self.assertFalse(o1.default)
        self.assertIsNone(o1.desc)

        o2 = BoolOption('meenie', default=True)
        self.assertEqual(o2.name, 'meenie')
        self.assertTrue(o2.default)
        self.assertIsNone(o2.desc)

        o3 = BoolOption('moe', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertFalse(o3.default)
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

    def testChoiceOptions(self):

        try:
            o1 = ChoiceOption('eeenie')
            self.fail("Didn't catch missing choices")
        except:
            pass

        o1 = ChoiceOption('eeenie', ['a', 'b', 'c', ])
        self.assertEqual(o1.name, 'eeenie')
        self.assertEqual(o1.choices, ['a', 'b', 'c'])
        self.assertFalse(o1.default)
        self.assertIsNone(o1.desc)

        o2 = ChoiceOption('meenie', ['a', 'b', 'c', ], default='b')
        self.assertEqual(o2.name, 'meenie')
        self.assertEqual(o1.choices, ['a', 'b', 'c'])
        self.assertEqual(o2.default, 'b')
        self.assertIsNone(o2.desc)

        o3 = ChoiceOption('moe', ['a', 'b', 'c', ], default='c', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertEqual(o1.choices, ['a', 'b', 'c'])
        self.assertEqual(o3.default, 'c')
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

    def testFloatOptions(self):

        o1 = FloatOption('eeenie')
        self.assertEqual(o1.name, 'eeenie')
        self.assertIsNone(o1.default)
        self.assertIsNone(o1.desc)

        o2 = FloatOption('meenie', default=17.2)
        self.assertEqual(o2.name, 'meenie')
        self.assertEqual(o2.default, 17.2)
        self.assertIsNone(o2.desc)

        o3 = FloatOption('moe', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertIsNone(o3.default)
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

    def testIntOptions(self):

        o1 = IntOption('eeenie')
        self.assertEqual(o1.name, 'eeenie')
        self.assertFalse(o1.default)
        self.assertIsNone(o1.desc)

        o2 = IntOption('meenie', default=314159)
        self.assertEqual(o2.name, 'meenie')
        self.assertEqual(o2.default, 314159)
        self.assertIsNone(o2.desc)

        o3 = IntOption('moe', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertIsNone(o3.default)
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

    def testListOptions(self):

        # XXX NEEDS 0 <= minLen <= maxLen <= MAX_INT

        o1 = ListOption('eeenie')
        self.assertEqual(o1.name, 'eeenie')
        self.assertFalse(o1.default)
        self.assertIsNone(o1.desc)

        o2 = ListOption('meenie', default=[])
        self.assertEqual(o2.name, 'meenie')
        self.assertEqual(o2.default, [])
        self.assertIsNone(o2.desc)

        o3 = ListOption('moe', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertEqual(o3.default, None)
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

    def testStrOptions(self):

        o1 = StrOption('eeenie')
        self.assertEqual(o1.name, 'eeenie')
        self.assertIsNone(o1.default)
        self.assertIsNone(o1.desc)

        o2 = StrOption('meenie', default='abc')
        self.assertEqual(o2.name, 'meenie')
        self.assertEqual(o2.default, 'abc')
        self.assertIsNone(o2.desc)

        o3 = StrOption('moe', desc='george')
        self.assertEqual(o3.name, 'moe')
        self.assertIsNone(o3.default)
        self.assertEqual(o3.desc, "george")

        # XXX No json yet

if __name__ == '__main__':
    unittest.main()
