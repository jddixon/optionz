#!/usr/bin/env python3

# testMetaClasses.py

import os
import time
import unittest

from rnglib import SimpleRNG


class TestMetaClasses (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # singleton -----------------------------------------------------

    def testSingleton(self):

        class Singleton(type):
            """
            Classes derived from this metaclass will indeed be singletons.
            """
            _instance = None

            def __call__(cls, *args, **kwargs):
                if not cls is Singleton._instance:
                    Singleton._instance = cls
                return Singleton._instance

        class Foo(metaclass=Singleton):
            pass

        foo1 = Foo()
        foo2 = Foo()

        # addresses are the same, so this is a true singleton
        self.assertTrue(foo1 is foo2)

    def testMetaclassWithKeywords(self):
        """
        """

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

        class MyOption(metaclass=MetaOption, a=15, b=25):
            """ Notice the items being passed as parameters to the class """
            pass

        obj = MyOption()

        self.assertFalse(obj is None)
        self.assertEqual(len(obj.__dict__), 0)
        self.assertEqual(obj.a, 15)
        self.assertEqual(obj.b, 25)


if __name__ == '__main__':
    unittest.main()
