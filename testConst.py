#!/usr/bin/env python3

# testConst.py

import os
import time
import unittest

from rnglib import SimpleRNG

X = 9123


class TestConst (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())   # the default, ne?

    def tearDown(self):
        pass

    def testConst(self):
        class Foo(object):
            A = 15

            @property
            def B(self):
                return 997

        # X is not a constnat ---------------------------------------
        global X
        self.assertEqual(X, 9123)
        X = -42
        self.assertEqual(X, -42)

        # A is not a constant ---------------------------------------
        foo = Foo()
        self.assertEqual(foo.A, 15)

        foo.A = 17
        self.assertEqual(foo.A, 17)

        # is B a constant? ------------------------------------------

        # at the instance level, yes, sort of -------------
        try:
            foo.B = 42
            self.fail("assigned value to foo.B")
        except AttributeError:
            pass
        self.assertEqual(foo.B, 997)

        # at the class level, no --------------------------
        self.assertEqual(str(type(Foo.B)), "<class 'property'>")
        try:
            Foo.B = 42
        except AttributeError:
            self.fail("got AttributeError assigning an int to Foo.B")

        self.assertEqual(Foo.B, 42)         # class attribute overridden
        self.assertEqual(foo.B, 42)         # instance attribute also

    def testBreakingIronA(self):
        """
        Shows that setting a new __setattr__ at the instance level
        provides no benefit: it is simply ignored.
        """

        def mySetAttr(self, name, value):
            self.__dict__[name] = value

        class IronMan(object):

            class IronError(TypeError):
                pass

            def __setattr__(self, name, value):
                if name in self.__dict__:
                    raise self.IronError("Can't change constant %s" % name)
                self.__dict__[name] = value

            def __delattr__(self, name):
                if name in self.__dict__:
                    raise self.IronError("Can't delete constant %s" % name)
                else:
                    raise NameError(name)

        e = IronMan()
        e.x = 4421                  # our new constant value
        try:
            e.x = 92
            self.fail("assigned value to IronMan constant")
        except IronMan.IronError:
            pass
        self.assertEqual(e.x, 4421)

        # set aninstance-level setter
        e.__setattr__ = mySetAttr
        self.assertEqual(e.__setattr__, mySetAttr)

        # attempts to change the constant fail
        try:
            e.x = 992
            self.fail("successfully modified constant e.x")
        except IronMan.IronError:
            pass
        self.assertEqual(e.x, 4421)

    def testBreakingIronB(self):
        """
        Shows that a seemingly safe constant can be changed by simply
        overriding __setattr__ at the IronMan class level.
        """

        def mySetAttr(self, name, value):
            self.__dict__[name] = value

        class IronMan(object):

            class IronError(TypeError):
                pass

            def __setattr__(self, name, value):
                if name in self.__dict__:
                    raise self.IronError("Can't change constant %s" % name)
                self.__dict__[name] = value

            def __delattr__(self, name):
                if name in self.__dict__:
                    raise self.IronError("Can't delete constant %s" % name)
                else:
                    raise NameError(name)

        d = IronMan()
        d.X = 47                        # we define a constant
        try:
            d.X = 92
            self.fail("assigned value to IronMan constant")
        except IronMan.IronError:
            pass
        self.assertEqual(d.X, 47)

        # However, modify the class-level setter and the instance's idea of
        # the 'constant can be changed
        IronMan.__setattr__ = mySetAttr
        self.assertEqual(IronMan.__setattr__, mySetAttr)
        d.X = 17
        self.assertEqual(d.X, 17)

if __name__ == '__main__':
    unittest.main()
