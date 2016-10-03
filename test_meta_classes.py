#!/usr/bin/env python3
# testMetaClasses.py

""" Test metaclass construction. """

import unittest

from optionz import optionz_maker, Singleton, MetaOption


class TestMetaClasses(unittest.TestCase):
    """ Test metaclass construction. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # generic test(s) -----------------------------------------------

    def test_metaclass_with_keywords(self):
        """ Test passing metaclass attributes as keywords.  """

        class MyOption(metaclass=MetaOption, a__=15, b__=25):
            """ Notice the items being passed as parameters to the class """
            pass

        obj = MyOption()

        self.assertFalse(obj is None)
        self.assertEqual(len(obj.__dict__), 0)
        self.assertEqual(obj.a__, 15)
        self.assertEqual(obj.b__, 25)

    # singleton -----------------------------------------------------

    def test_singleton(self):
        """ Verify that a singleton really is such. """

        class Foo(metaclass=Singleton):
            """ Simplest singleton. """
            pass

        foo1 = Foo()
        foo2 = Foo()

        # addresses are the same, so this is a true singleton
        self.assertTrue(foo1 is foo2)

    def test_optionz_as_singleton(self):
        """ Test an Optionz object as a singleton. """

        class Moo(Singleton, metaclass=MetaOption):
            """ Test a MetaOption singleton. """
            pass

        moo1 = Moo()
        moo2 = Moo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(moo1 is moo2)

    def test_singleton_with_keywords(self):
        """ Test an options singleton with attributes passed as parameters."""

        kwargs = {'a79': 79, 'b__': 92, 'c__': 'george'}

        class Koo(Singleton, metaclass=MetaOption, **kwargs):
            """ To be set up as a singleton with keywords. """
            pass

        koo1 = Koo()
        koo2 = Koo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(koo1 is koo2)

        #####################################################
        # now FAILS: type object 'Moo' has no attribute 'a79'
        self.assertEqual(koo1.a79, 79)
        #####################################################

        self.assertEqual(koo1.b__, 92)
        self.assertEqual(koo1.c__, 'george')

        # immutability the Python way
        try:
            koo1.a79 = 997
            self.fail(
                "successfully changed attribute value")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(koo1.a79, 79)

        try:
            Koo.a79 = 31479926536
            self.fail(
                "successfully changed attribute value")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(Koo.a79, 79)
        self.assertEqual(koo1.a79, 79)

    def test_optionz_maker(self):
        """ Test another Optionz singleton created with keyword parameters."""

        kwargs = {'a13': 13, 'b__': 1947, 'c__': 'mike'}

        koo = optionz_maker(**kwargs)

        koo1 = koo()
        koo2 = koo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(koo1 is koo2)

        #####################################################################
        # NOW FAILS: "AttributeError: type object 'Moo' has no attribute 'a13'
        self.assertEqual(koo1.a13, 13)
        #####################################################################

        self.assertEqual(koo1.b__, 1947)
        self.assertEqual(koo1.c__, 'mike')

        # immutability the Python way
        try:
            koo1.a13 = 1066
            self.assertEqual(koo1.a13, 1066)
            self.fail(
                "successfully changed instance attribute")  # pragma: no cover
        except AttributeError:
            pass

        # we want this assignment to fail
        try:
            koo.a13 = 2718281828459
            self.fail(
                "successfully changed class attribute")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(koo.a13, 13)

        # we want this value to be unchanged as well
        self.assertEqual(koo1.a13, 13)

if __name__ == '__main__':
    unittest.main()
