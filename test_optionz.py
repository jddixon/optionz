#!/usr/bin/env python3
# testOptionz.py

""" Test the basic Optionz classes. """

import time
import unittest

from rnglib import SimpleRNG
from optionz import Optionz as Z
from optionz import (ValType, BoolOption, ChoiceOption,
                     FloatOption, IntOption, ListOption, StrOption)


class TestOptionz(unittest.TestCase):
    """ Test the basic Optionz classes. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_bare_optionz(self):
        """ Create an Optionz instance, check for expected attibutes. """

        my_optz = Z('fred')
        self.assertEqual(my_optz.name, 'fred')
        self.assertEqual(my_optz.desc, None)
        self.assertEqual(my_optz.epilog, None)
        self.assertEqual(len(my_optz), 0)

        my_optz = Z('frank', 'frivolous', 'fabulous')
        self.assertEqual(my_optz.name, 'frank')
        self.assertEqual(my_optz.desc, 'frivolous')
        self.assertEqual(my_optz.epilog, 'fabulous')
        self.assertEqual(len(my_optz), 0)

    def test_z_option(self):
        """ Populate an Optionz object, check for expected attr. """

        z_name = self.rng.nextFileName(8)
        z_desc = self.rng.nextFileName(64)
        z_epilog = self.rng.nextFileName(64)

        my_optz = Z(z_name, z_desc, z_epilog)

        self.assertEqual(my_optz.name, z_name)
        self.assertEqual(my_optz.desc, z_desc)
        self.assertEqual(my_optz.epilog, z_epilog)
        self.assertEqual(len(my_optz), 0)

        # booleans --------------------------------------------------

        b_dflt_val = True
        b_desc = "I'm small"
        bool_opt = BoolOption('bO', default=b_dflt_val, desc=b_desc)
        self.assertEqual(bool_opt.name, 'bO')
        self.assertEqual(bool_opt.default, b_dflt_val)
        self.assertEqual(bool_opt.desc, b_desc)

        #                        name    valType     default    desc
        b_check = my_optz.add_option('bO', ValType.BOOL, b_dflt_val, b_desc)
        self.assertEqual(len(my_optz), 1)
        self.assertEqual(bool_opt, b_check)

        # choice lists ----------------------------------------------

        # NOTE We should probably require that list elements be of
        # compatible types.  For the moment we just assume that elements
        # are all strings.

        # succeeds if default in list of choices ----------
        my_size = 2 + self.rng.nextInt16(4)     # so in [2..5]
        choice = self.rng.nextFileName(8)
        choices = [choice]

        while len(choices) < my_size:
            if not choice in choices:
                choices.append(choice)
            choice = self.rng.nextFileName(8)

        c_dflt_val = choices[self.rng.nextInt16(my_size)]
        c_desc = 'a list'
        choice_opt = ChoiceOption('cO', choices, c_dflt_val, c_desc)
        self.assertEqual(choice_opt.name, 'cO')
        self.assertEqual(choice_opt.choices, choices)
        self.assertEqual(choice_opt.default, c_dflt_val)
        self.assertEqual(choice_opt.desc, "a list")

        # fails if default is NOT in list of choices ------
        my_size = 2 + self.rng.nextInt16(4)     # so in [2..5]
        choice = self.rng.nextFileName(8)
        b_choices = [choice]

        while len(b_choices) < my_size:
            if not choice in b_choices:
                b_choices.append(choice)
            choice = self.rng.nextFileName(8)

        dflt_val = self.rng.nextFileName(8)
        while dflt_val in choices:
            dflt_val = self.rng.nextFileName(8)

        try:
            bad_choice_opt = ChoiceOption('bC', choices,
                                          default=dflt_val, desc="a list")
            self.fail('successfully added default value not in list of choices')
        except:
            pass

        c_check = my_optz.add_choice_option('cO', choices, c_dflt_val, c_desc)
        self.assertEqual(len(my_optz), 2)
        self.assertEqual(choice_opt, c_check)

        # floats ----------------------------------------------------

        f_dflt_val = self.rng.nextReal()
        f_desc = 'bubbly'
        float_opt = FloatOption('fO', default=f_dflt_val, desc=f_desc)
        self.assertEqual(float_opt.name, 'fO')
        self.assertEqual(float_opt.default, f_dflt_val)
        self.assertEqual(float_opt.desc, f_desc)

        #                        name    valType     default    desc
        f_check = my_optz.add_option('fO', ValType.FLOAT, f_dflt_val, f_desc)
        self.assertEqual(len(my_optz), 3)
        self.assertEqual(float_opt, f_check)

        # ints ------------------------------------------------------

        i_dflt_val = self.rng.nextInt32()
        i_desc = 'discrete'
        int_opt = IntOption('iO', default=i_dflt_val, desc=i_desc)
        self.assertEqual(int_opt.name, 'iO')
        self.assertEqual(int_opt.default, i_dflt_val)
        self.assertEqual(int_opt.desc, i_desc)

        #                        name    valType     default    desc
        i_check = my_optz.add_option('iO', ValType.INT, i_dflt_val, i_desc)
        self.assertEqual(len(my_optz), 4)
        self.assertEqual(int_opt, i_check)

        # lists -----------------------------------------------------

        size_val = self.rng.nextInt16()
        # select polarity of size randomly
        if self.rng.nextBoolean():
            size_val = - size_val
        l_desc = "chunky"

        list_opt = ListOption('lO', default=size_val, desc=l_desc)
        self.assertEqual(list_opt.name, 'lO')
        self.assertEqual(list_opt.default, size_val)
        self.assertEqual(list_opt.size, size_val)
        self.assertEqual(list_opt.desc, l_desc)

        zero_val = 0
        var_list_opt = ListOption('zO', default=zero_val, desc="skinny")
        self.assertEqual(var_list_opt.name, 'zO')
        self.assertEqual(var_list_opt.default, zero_val)
        self.assertEqual(var_list_opt.desc, "skinny")

        #                        name    valType     default    desc
        l_check = my_optz.add_option('lO', ValType.LIST, size_val, l_desc)
        self.assertEqual(len(my_optz), 5)
        self.assertEqual(list_opt, l_check)

        # strings ---------------------------------------------------

        s_dflt_val = self.rng.nextFileName(12)
        s_desc = "wiggly"

        str_opt = StrOption('sO', default=s_dflt_val, desc=s_desc)
        self.assertEqual(str_opt.name, 'sO')
        self.assertEqual(str_opt.default, s_dflt_val)
        self.assertEqual(str_opt.desc, s_desc)

        #                        name    valType     default    desc
        s_check = my_optz.add_option('sO', ValType.STR, s_dflt_val, s_desc)
        self.assertEqual(len(my_optz), 6)
        self.assertEqual(str_opt, s_check)


if __name__ == '__main__':
    unittest.main()
