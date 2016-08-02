#!/usr/bin/env python3

# testClassMaker.py

import os
import time
import unittest

from rnglib import SimpleRNG
from optionz import _BaseOption, Option


class EmptyClass():
    pass


def simpleAdder(self, a, b):
    return a + b


class TestClassMaker (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def testMaker(self):
        class MetaOption(type):

            @classmethod
            def __prepare__(metacls, name, bases, **kwargs):
                """
                Optional.  Here we use kwargs to set attributes of the
                class. Need to return a dictionary-like object.
                """
                return dict(kwargs)

            def __new__(cls, name, bases, namespace, **kwargs):
                """
                Creates the class; may need to cast namespace to dict.
                Omit kwargs from call to __new__().
                """
                return super().__new__(cls, name, bases, namespace)

            def __init__(cls, name, bases, namespace, **kwargs):
                """
                Omit kwargs from call to __init__().
                """
                super().__init__(name, bases, namespace)

            def foo(self):
                return 42

        class MyOption(metaclass=MetaOption, a=15, b=25):
            """ Notice the items being passed as parameters to the class """

        class ClassMaker(object):

            def __init__(self):
                self._Foo = MyOption

                # adding functions to the class: --------------------

                #             'object'      'instance'  'owner'
                self._Foo.c = self.c.__get__(self._Foo, ClassMaker)
                self._Foo.d = self.d.__get__(self._Foo, ClassMaker)

                # end adding funcions -------------------------------

            def inst(self):
                return self._Foo

            def c(self):
                return 98

            def d(self):
                return 199

        Maker1 = ClassMaker()
        Maker2 = ClassMaker()
        self.assertFalse(Maker1 is None)
        self.assertFalse(Maker2 is None)
        self.assertTrue(Maker1 is not Maker2)

        foo1 = Maker1.inst()

        # attributes added by parameters to MyOption
        self.assertEqual(foo1.a, 15)
        self.assertEqual(foo1.b, 25)

        # methods added programmtically by ClassMaker
        self.assertEqual(foo1.c(), 98)
        self.assertEqual(foo1.d(), 199)

if __name__ == '__main__':
    unittest.main()
