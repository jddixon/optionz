#!/usr/bin/env python3
# testConst.py

""" Test behavior of 'constants'. """

import time
import unittest

from rnglib import SimpleRNG

X9123 = 9123


class TestConst(unittest.TestCase):
    """ Test behavior of 'constants'. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())   # the default, ne?

    def tearDown(self):
        pass

    def test_module_level(self):
        """ Test module-level "constants". """

        # X9123 is not a constnat -----------------------------------
        global X9123
        self.assertEqual(X9123, 9123)
        X9123 = -42
        self.assertEqual(X9123, -42)

    def test_const(self):
        """ Test class 'constants'. """

        # pylint: disable=too-few-public-methods
        class Foo(object):
            """ Class whose only purpose is to carry a 'constant'. """
            a15 = 15

            @property
            def b997(self):
                """ Return an integer, a true-ish constant. """
                return 997

        # a15 is not a constant ---------------------------------------
        foo2 = Foo()
        self.assertEqual(foo2.a15, 15)

        foo2.a15 = 17
        self.assertEqual(foo2.a15, 17)

        # is b997 a constant? ------------------------------------------

        # at the instance level, yes, sort of -------------
        try:
            foo2.b997 = 42
            self.fail("assigned value to foo2.b997")    # pragma: no cover
        except AttributeError:
            pass
        self.assertEqual(foo2.b997, 997)

        # at the class level, no --------------------------
        self.assertEqual(str(type(Foo.b997)), "<class 'property'>")
        try:
            Foo.b997 = 42
        except AttributeError:
            self.fail(
                "got AttributeError assigning an int to Foo.b997")

        self.assertEqual(Foo.b997, 42)         # class attribute overridden
        self.assertEqual(foo2.b997, 42)      # instance attribute also

    def test_breaking_iron(self):
        """
        Shows that setting a new __setattr__ at the instance level
        provides no benefit: it is simply ignored.
        """

        def my_set_attr(self, name, value):
            """ Define a local set-attribute function. """
            self.__dict__[name] = value

        # pylint: disable=too-few-public-methods
        class IronMan(object):
            """ A class which we trust will be bullet-proof."""

            class IronError(TypeError):
                """ Dummy error. """
                pass

            def __setattr__(self, name, value):
                """ Private function setting a dictionary value."""

                if name in self.__dict__:
                    raise self.IronError("Can't change constant %s" % name)
                self.__dict__[name] = value

            # never used
            def __delattr__(self, name):        # pragma: no cover
                """ Private function deleting key/value from dictionary. """
                if name in self.__dict__:
                    raise self.IronError("Can't delete constant %s" % name)
                else:
                    raise NameError(name)

        iron = IronMan()
        # pylint: disable=attribute-defined-outside-init
        iron.x__ = 47                        # we define a constant
        try:
            # pylint: disable=attribute-defined-outside-init
            iron.x__ = 92
            self.fail("assigned value to IronMan constant")  # pragma: no cover
        except IronMan.IronError:
            pass
        self.assertEqual(iron.x__, 47)

        # However, modify the class-level setter and the instance's idea of
        # the 'constant can be changed
        IronMan.__setattr__ = my_set_attr
        self.assertEqual(IronMan.__setattr__, my_set_attr)
        # pylint: disable=attribute-defined-outside-init
        iron.x__ = 17
        self.assertEqual(iron.x__, 17)


if __name__ == '__main__':
    unittest.main()
