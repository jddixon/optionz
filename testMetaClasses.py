#!/usr/bin/env python3

# testMetaClasses.py

import os
import time
import unittest

from optionz import optionzMaker, Singleton, MetaOption


class TestMetaClasses (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # generic test(s) -----------------------------------------------

    def testMetaclassWithKeywords(self):
        """
        """

        class MyOption(metaclass=MetaOption, a=15, b=25):
            """ Notice the items being passed as parameters to the class """
            pass

        obj = MyOption()

        self.assertFalse(obj is None)
        self.assertEqual(len(obj.__dict__), 0)
        self.assertEqual(obj.a, 15)
        self.assertEqual(obj.b, 25)

    # singleton -----------------------------------------------------

    def testSingleton(self):

        class Foo(metaclass=Singleton):
            pass

        foo1 = Foo()
        foo2 = Foo()

        # addresses are the same, so this is a true singleton
        self.assertTrue(foo1 is foo2)

    def testOptionzAsSingleton(self):

        class Moo(Singleton, metaclass=MetaOption):
            pass

        moo1 = Moo()
        moo2 = Moo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(moo1 is moo2)

    def testOptionzAsSingleton(self):

        class Moo(Singleton, metaclass=MetaOption):
            pass

        moo1 = Moo()
        moo2 = Moo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(moo1 is moo2)

    def testOptionzAsSingletonWithKeywords(self):

        kwargs = {'a': 15, 'b': 92, 'c': 'george'}

        class Koo(Singleton, metaclass=MetaOption, **kwargs):
            pass

        koo1 = Koo()
        koo2 = Koo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(koo1 is koo2)

        self.assertEqual(koo1.a, 15)
        self.assertEqual(koo1.b, 92)
        self.assertEqual(koo1.c, 'george')

        # immutability the Python way
        try:
            koo1.a = 997
            self.fail(
                "successfully changed attribute value")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(koo1.a, 15)

        try:
            Koo.a = 31415926536
            self.fail(
                "successfully changed attribute value")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(Koo.a, 15)
        self.assertEqual(koo1.a, 15)

    def testOptionzMaker(self):

        kwargs = {'a': 13, 'b': 1947, 'c': 'mike'}

        Koo = optionzMaker(**kwargs)

        koo1 = Koo()
        koo2 = Koo()

        # addresses are the same, so this is a true singleton too
        self.assertTrue(koo1 is koo2)

        self.assertEqual(koo1.a, 13)
        self.assertEqual(koo1.b, 1947)
        self.assertEqual(koo1.c, 'mike')

        # immutability the Python way
        try:
            koo1.a = 1066
            self.assertEqual(koo1.a, 1066)
            self.fail(
                "successfully changed instance attribute")  # pragma: no cover
        except AttributeError:
            pass

        # we want this assignment to fail
        try:
            Koo.a = 2718281828459
            self.fail(
                "successfully changed class attribute")   # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(Koo.a, 13)

        # we want this value to be unchanged as well
        self.assertEqual(koo1.a, 13)

if __name__ == '__main__':
    unittest.main()
