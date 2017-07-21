#!/usr/bin/env python3
# testClassMaker.py

""" Test metaclass behavior. """

import time
import unittest

from rnglib import SimpleRNG

# pylint:disable=too-few-public-methods


class EmptyClass():
    """ Just an empty class. """
    pass

# pylint:disable=unused-argument


def simple_adder(self, a__, b__):
    """ The simplest adder function. """
    return a__ + b__


class TestClassMaker(unittest.TestCase):
    """ Test metaclass behavior. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_maker(self):
        """Actually test making a class."""

        # pylint doesn't see use below
        # pylint: disable=unused-variable
        class MetaOption(type):
            """ The metaclass definition. """

            @classmethod
            def __prepare__(mcs, name, bases, **kwargs):
                """
                Optional.  Here we use kwargs to set attributes of the
                class. Need to return a dictionary-like object.
                """
                _, _ = name, bases
                return dict(kwargs)

            def __new__(mcs, name, bases, namespace, **kwargs):
                """
                Creates the class; may need to cast namespace to dict.
                Omit kwargs from call to __new__().
                """
                return super().__new__(mcs, name, bases, namespace)

            def __init__(cls, name, bases, namespace, **kwargs):
                """
                Omit kwargs from call to __init__().
                """
                super().__init__(name, bases, namespace)

            # pylint: disable=no-self-use
            def foo42(cls):
                """ Nonsensical function. """
                return 42

        class MyOption(metaclass=MetaOption, a15=15, b25=25):
            """ Notice the items being passed as parameters to the class """

        class ClassMaker(object):
            """ Trivial class wherein we construct a subclass. """

            def __init__(self):
                self._foo = MyOption

                # adding functions to the class: --------------------

                #               'object'      'instance'    'owner'
                # pylint: disable=no-member
                self._foo.c98 = self.c98.__get__(self._foo, ClassMaker)
                # pylint: disable=no-member
                self._foo.d199 = self.d199.__get__(self._foo, ClassMaker)

                # end adding funcions -------------------------------

            def inst(self):
                """ Return the subclass member. """
                return self._foo

            # pylint: disable=no-self-use
            def c98(self):
                """ Return an integer. """
                return 98

            # pylint: disable=no-self-use
            def d199(self):
                """ Return another integer. """
                return 199

        maker1 = ClassMaker()
        maker2 = ClassMaker()
        self.assertFalse(maker1 is None)
        self.assertFalse(maker2 is None)
        self.assertTrue(maker1 is not maker2)

        foo1 = maker1.inst()

        # attributes added by parameters to MyOption
        # pylint: disable=no-member
        self.assertEqual(foo1.a15, 15)
        # pylint: disable=no-member
        self.assertEqual(foo1.b25, 25)

        # methods added programmatically by ClassMaker
        self.assertEqual(foo1.c98(), 98)
        self.assertEqual(foo1.d199(), 199)


if __name__ == '__main__':
    unittest.main()
