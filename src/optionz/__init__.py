#!/usr/bin/env python3

""" Option class and supporting cast. """

import enum

# optionz/optionz/__init__.py

__all__ = ['__version__', '__version_date__',
           # new functions
           'dump_options',
           # functions
           'optionz_maker',
           # classes
           'Singleton', 'MetaOption',
           # PROVISIONAL:
           'Optionz', 'ValType',
           'ZOption', 'BoolOption', 'ChoiceOption', 'FloatOption',
           'IntOption', 'ListOption', 'StrOption', ]

__version__ = '0.2.11'
__version_date__ = '2017-11-28'

JUST_HEADERS = 'OPTION VALUE\n'


def dump_options(ns_, with_headers=True):
    """
    Serialize Namespace for output as sorted, formatted list.

    This is an aid for use with argparse's ArgumentParser, which
    outputs Namespaces.  It prints a table of options and their values,
    breaking out any list values to be tabulated separately.

    If with_headers, precede the table of options with an
      OPTION VALUE
    line.
    """

    if ns_ is None:
        retval = ''
        if with_headers:
            retval = JUST_HEADERS
        return retval

    items = sorted(ns_.__dict__.items())        # a list of pairs
    if not items:
        retval = ''
        if with_headers:
            retval = JUST_HEADERS
        return retval

    # We expect only pairs whose LHS is a string and whose RHIS is either
    # a scalar (int, float, str) or a list.  Those with list values are
    # handled separately.

    scalar_pairs = []
    list_pairs = []
    width_lhs = 0
    if with_headers:
        width_lhs = 6           # for the word 'OPTION'

    for pair in items:
        lhs = pair[0]
        rhs = pair[1]
        if isinstance(rhs, list):
            list_pairs.append(pair)
        else:
            if len(lhs) > width_lhs:
                width_lhs = len(lhs)
            scalar_pairs.append(pair)

    if with_headers:
        fmt = "%%-%ds %%s" % width_lhs
        output = [fmt % ('OPTION', 'VALUE')]
    else:
        output = []

    if scalar_pairs:
        for pair in scalar_pairs:
            lhs = pair[0]
            rhs = pair[1]
            if isinstance(rhs, (str, bool)):
                fmt = "%%-%ds %%s" % width_lhs
            elif isinstance(rhs, int):
                fmt = "%%-%ds %%d" % width_lhs
            elif isinstance(rhs, float):
                fmt = "%%-%ds %%f" % width_lhs
            else:
                fmt = "%%-%ds %%s" % width_lhs
            text = fmt % (lhs, rhs)
            output.append(text)

    if list_pairs:
        for pair in list_pairs:
            lhs = pair[0]
            rhs = pair[1]
            output.append(('\n' + lhs + 'S:').upper())
            for value in rhs:
                if isinstance(value, (str, bool)):
                    text = "    %s" % value
                elif isinstance(value, int):
                    text = "    %d" % value
                elif isinstance(value, float):
                    text = "    %f" % value
                else:
                    text = "    %s" % value
                output.append(text)

    return '\n'.join(output) + '\n'

# EXPERIMENTAL ======================================================


class OptionzError(RuntimeError):
    """ Optionz-related exceptions class. """
    pass


class Singleton(type):
    """
    Classes derived from this metaclass will indeed be singletons.
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        # DEBUG
        print("entering Singleton.__call__")
        # END
        if cls._instance is None:
            # DEBUG
            print("    ._instance IS None")
            print("        about to call super() = type()")
            # END
            cls._instance = super().__call__(*args, **kwargs)
        # DEBUG
        else:
            print("    _instance is NOT None")
        # END
        return cls._instance


class Immutable(object):
    """ Define immutable class/object -- currently unused. """

    def __setattr__(self, name, value):
        """ Overrides standard function. """
        raise AttributeError("attempt to change immutable value")


class MetaOption(type):
    """ Metaclass for Option. """

    @classmethod
    def __prepare__(mcs, **kwargs):                 # name?, bases?
        """
        Optional.  Here we use kwargs to set attributes of the
        class. Need to return a dictionary-like object.
        """
        # DEBUG
        print("\n__PREPARE__")
        # END
        return dict(kwargs)

    def __new__(mcs, name, bases, namespace):       # , **kwargs):
        """
        Creates the class; may need to cast namespace to dict.
        Omit kwargs from call to __new__().
        """
        # DEBUG
        print("__NEW__")
        # END
        obj = type.__new__(mcs, name, bases, namespace)
        print("    DEBUG: __new__(name=%s) succeeded" % name)
        return obj

    def __init__(cls, name, bases, namespace):      # , **kwargs):
        """
        Omit kwargs from call to __init__().
        """
        # DEBUG
        print("__INIT__")
        # END
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        """ Instantiates instances of the class. """
        # DEBUG
        print("__CALL__, cls = %s" % cls.__name__)
        # END
        # gets "type() takes 1 or 3 arguments"
        obj = type.__call__(cls, *args, **kwargs)        # ERROR ??
        print("    DEBUG: __call__ succeeded")
        return obj

    def __setattr__(cls, key, value):
        raise AttributeError("attempt to change immutable value")

# def attrSetter(self, key, value):
#    raise AttributeError("attempt to change immutable value")


def optionz_maker(**kwargs):
    """ Return an Options class inheriting from Singleton and MetaOption. """
    class MyOptions(Singleton, metaclass=MetaOption, **kwargs):
        """ That Options class. """
        pass
    return MyOptions

#####################################################################
# NOTE EVEN MORE PROVISIONAL
#####################################################################


class _BaseOption(object):
    """ Unused base class for options. """
    pass


class Option(_BaseOption):
    """
    Carrier for a collection of what we hope are immutable key-value
    pairs.  These are passed to the constructor as kwargs.
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not other or not isinstance(other, _BaseOption):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    __hash__ = None         # since we have defined __eq__

    def __contains__(self, key):
        return key in self.__dict__

# END EVEN MORE PROVISIONAL #########################################


class ValType(enum.IntEnum):
    """ Enumerate argument types currently supported. """
    BOOL = 1
    CHOICE = 2
    FLOAT = 3
    INT = 4
    LIST = 5
    STR = 6


class Optionz(object):
    """
    Metadata used in interpreting a sequence of command line
    arguments.
    """

    def __init__(self, name, desc=None, epilog=None):
        self._name = name
        self._desc = desc           # short, top of help message
        self._epilog = epilog       # footer for help message
        self._z_options = []
        self._z_map = {}

    @property
    def name(self):
        """ Return the name associated with a help message. """
        return self._name

    @property
    def desc(self):
        """ Return the main 'description' part of a help message. """
        return self._desc

    @property
    def epilog(self):
        """ Return the 'epilog' part of a help message. """
        return self._epilog

    # Possibly want to add 'def add_choice_option()' and 'def add_list_option'
    # to handle additional parameters

    def add_option(self, name, val_type, default=None, desc=None):
        """
        Add metadata used in handling a command line argument, including its
        name, base type (int, str, etc), default value, and the description
        used in help messages.
        """
        if val_type < ValType.BOOL or val_type > ValType.STR:
            raise OptionzError('unrecognized val_type %d', val_type)
        if name in self._z_map:
            raise ValueError("duplicate option name '%s'" % name)

        if val_type == ValType.BOOL:
            new_option = BoolOption(name, default, desc)
        elif val_type == ValType.FLOAT:
            new_option = FloatOption(name, default, desc)
        elif val_type == ValType.INT:
            new_option = IntOption(name, default, desc)
        elif val_type == ValType.LIST:
            new_option = ListOption(name, default, desc)
        elif val_type == ValType.STR:
            new_option = StrOption(name, default, desc)
        else:
            raise OptionzError("uncaught bad option type %d" % val_type)

        self._z_map[name] = new_option
        self._z_options.append(new_option)
        return new_option

    def add_choice_option(self, name, choices, default=None, desc=None):
        """
        Add choice metadata to a collection of command line options.
        """
        if name in self._z_map:
            raise ValueError("duplicate option name '%s'" % name)
        new_option = ChoiceOption(name, choices, default, desc)
        self._z_map[name] = new_option
        self._z_options.append(new_option)
        return new_option

    def __len__(self):
        """
        Return the number of distinct option types.  A single set of
        choices, for example, or a list of variable length will each
        increase this value by one.  In other words, it is not generally
        the same as the number of arguments in any particular command line.

        """
        return len(self._z_options)


class ZOption(object):
    """ Basic attributes of an Option: name, type, default, desc."""

    def __init__(self, name, val_type, default, desc):
        self._name = name
        self._type = val_type
        self._default = default
        self._desc = desc       # brief, used in usage()

    @property
    def name(self):
        """ Return the name of an Option. """
        return self._name

    @property
    def default(self):
        """ Return the default value of an Option. """
        return self._default

    @property
    def desc(self):
        """ Return the description associated with an Option. """
        return self._desc


class BoolOption(ZOption):
    """ Command line option of boolean type. """

    def __init__(self, name, default=False, desc=None):
        super().__init__(name, ValType.BOOL, default, desc)

    def __eq__(self, other):
        return isinstance(other, BoolOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc


class ChoiceOption(ZOption):
    """
    This implementation makes no attempt to make sure that the list
    of choices is homogeneous (all elements are of the same type) or
    otherwise sensible.
    """

    def __init__(self, name, choices, default=None, desc=None):
        super().__init__(name, ValType.CHOICE, default, desc)
        self._choices = [ch for ch in choices]

        if default and default not in choices:
            raise OptionzError("default value '%s' is not in %s's choices" % (
                default, name))

    @property
    def choices(self):
        """ returns a copy of the list of choices """
        return [ch for ch in self._choices]

    def __eq__(self, other):
        return isinstance(other, ChoiceOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc


class FloatOption(ZOption):
    """ Command line option of float type. """

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.FLOAT, default, desc)

    def __eq__(self, other):
        return isinstance(other, FloatOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc


class IntOption(ZOption):
    """ Command line option of int type. """

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.INT, default, desc)

    def __eq__(self, other):
        return isinstance(other, IntOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc


class ListOption(ZOption):
    """
    Here 'default' is interpreted as the number of elements in the
    list: 0 means any number, -N means up to N values inclusive
    may be supplied, and N > 0 means that exactly N values must
    be supplied.
    """

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.LIST, default, desc)

    # an alias
    @property
    def size(self):
        """ Return the default number of items in the list. """
        return self._default

    def __eq__(self, other):
        """ Whether instances are equal. """
        return isinstance(other, ListOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc


class StrOption(ZOption):
    """ Command line option of string type. """

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.STR, default, desc)

    def __eq__(self, other):
        return isinstance(other, StrOption) and \
            self._name == other.name and \
            self._default == other.default and \
            self._desc == other.desc
