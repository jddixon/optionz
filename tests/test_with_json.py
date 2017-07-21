#!/usr/bin/env python3
# testWithJson.py

""" Test serialization with Json. """

import time
import unittest

from rnglib import SimpleRNG
from optionz import(BoolOption, ChoiceOption,
                    FloatOption, IntOption, ListOption, StrOption)


class TestWithJson(unittest.TestCase):
    """ Test serialization with Json. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_bool_options(self):
        """ Interpret a string on the command line as a boolean value. """

        o1_ = BoolOption('eeenie')
        self.assertEqual(o1_.name, 'eeenie')
        self.assertFalse(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = BoolOption('meenie', default=True)
        self.assertEqual(o2_.name, 'meenie')
        self.assertTrue(o2_.default)
        self.assertIsNone(o2_.desc)

        o3_ = BoolOption('moe', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertFalse(o3_.default)
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet

    def test_choice_options(self):
        """ Test choices option where must use value from list. """
        try:
            # pylint: disable=no-value-for-parameter
            o1_ = ChoiceOption('eeenie')
            self.fail("Didn't catch missing choices")
        except TypeError:
            pass

        o1_ = ChoiceOption('eeenie', ['a', 'b', 'c', ])
        self.assertEqual(o1_.name, 'eeenie')
        self.assertEqual(o1_.choices, ['a', 'b', 'c'])
        self.assertFalse(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = ChoiceOption('meenie', ['a', 'b', 'c', ], default='b')
        self.assertEqual(o2_.name, 'meenie')
        self.assertEqual(o1_.choices, ['a', 'b', 'c'])
        self.assertEqual(o2_.default, 'b')
        self.assertIsNone(o2_.desc)

        o3_ = ChoiceOption('moe', ['a', 'b', 'c', ],
                           default='c', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertEqual(o1_.choices, ['a', 'b', 'c'])
        self.assertEqual(o3_.default, 'c')
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet

    def test_float_options(self):
        """
        Test float option, where string on command line is interpreted
        as a floating point value.
        """
        o1_ = FloatOption('eeenie')
        self.assertEqual(o1_.name, 'eeenie')
        self.assertIsNone(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = FloatOption('meenie', default=17.2)
        self.assertEqual(o2_.name, 'meenie')
        self.assertEqual(o2_.default, 17.2)
        self.assertIsNone(o2_.desc)

        o3_ = FloatOption('moe', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertIsNone(o3_.default)
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet

    def test_int_options(self):
        """
        Test IntOption, where string from command line is interpreted
        as an integer.
        """
        o1_ = IntOption('eeenie')
        self.assertEqual(o1_.name, 'eeenie')
        self.assertFalse(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = IntOption('meenie', default=314159)
        self.assertEqual(o2_.name, 'meenie')
        self.assertEqual(o2_.default, 314159)
        self.assertIsNone(o2_.desc)

        o3_ = IntOption('moe', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertIsNone(o3_.default)
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet

    def test_list_options(self):
        """
        Test ListOption, where a sequences of strings on the command
        line are accepted as a list.
        """

        # NOTE NEEDS 0 <= minLen <= maxLen <= MAX_INT

        o1_ = ListOption('eeenie')
        self.assertEqual(o1_.name, 'eeenie')
        self.assertFalse(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = ListOption('meenie', default=[])
        self.assertEqual(o2_.name, 'meenie')
        self.assertEqual(o2_.default, [])
        self.assertIsNone(o2_.desc)

        o3_ = ListOption('moe', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertEqual(o3_.default, None)
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet

    def test_str_options(self):
        """
        Test the base case, where a string from the command line is
        treated as a single string option value.
        """
        o1_ = StrOption('eeenie')
        self.assertEqual(o1_.name, 'eeenie')
        self.assertIsNone(o1_.default)
        self.assertIsNone(o1_.desc)

        o2_ = StrOption('meenie', default='abc')
        self.assertEqual(o2_.name, 'meenie')
        self.assertEqual(o2_.default, 'abc')
        self.assertIsNone(o2_.desc)

        o3_ = StrOption('moe', desc='george')
        self.assertEqual(o3_.name, 'moe')
        self.assertIsNone(o3_.default)
        self.assertEqual(o3_.desc, "george")

        # NOTE No json yet


if __name__ == '__main__':
    unittest.main()
