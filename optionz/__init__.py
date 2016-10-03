#!/usr/bin/env python3

""" Option class and supporting cast. """

import enum

# optionz/optionz/__init__.py

__all__ = ['__version__', '__version_date__',
           # functions
           'optionz_maker',
           # classes
           'Singleton', 'MetaOption',
           # PROVISIONAL:
           'Optionz', 'ValType',
           'ZOption', 'BoolOption', 'ChoiceOption', 'FloatOption',
           'IntOption', 'ListOption', 'StrOption',
           ]

__version__ = '0.2.0'
__version_date__ = '2016-10-03'


class OptionzError(RuntimeError):
    """ Optionz-related exceptions class. """
    pass


class Singleton(type):
    """
    Classes derived from this metaclass will indeed be singletons.
    """
    _instance = None

    def __new__(mcs, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = mcs
        return Singleton._instance


class Immutable(object):
    """ Define immutable class/object -- currently unused. """

    def __setattr__(self, name, value):
        """ Overrides standard function. """
        raise AttributeError("attempt to change immutable value")


class MetaOption(type):
    """ Metaclass for Option. """

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        """
        Optional.  Here we use kwargs to set attributes of the
        class. Need to return a dictionary-like object.
        """
        return dict(kwargs)

    def __new__(mcs, name, bases, namespace, **kwargs):
        """
        Creates the class; may need to cast namespace to dict.
        Omit kwargs from call to __new__().
        """
        Clz = super().__new__(mcs, name, bases, namespace)
        return Clz

    def __init__(cls, name, bases, namespace, **kwargs):
        """
        Omit kwargs from call to __init__().
        """
        super().__init__(name, bases, namespace)

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

        # DEBUG
        # print("eq:")
        #print("  self:  %s" % self.__dict__)
        #print("  other: %s" % other.__dict__)
        # END
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
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def epilog(self): return self._epilog

    # Possibly want to add 'def add_choice_option()' and 'def add_list_option'
    # to handle additional parameters

    def add_option(self, name, valType, default=None, desc=None):
        """
        Add metadata used in handling a command line argument, including its
        name, base type (int, str, etc), default value, and the description
        used in help messages.
        """
        if valType < ValType.BOOL or valType > ValType.STR:
            raise OptionzError('unrecognized valType %d', valType)
        if name in self._z_map:
            raise ValueError("duplicate option name '%s'" % name)

        if valType == ValType.BOOL:
            new_option = BoolOption(name, default, desc)
        elif valType == ValType.FLOAT:
            new_option = FloatOption(name, default, desc)
        elif valType == ValType.INT:
            new_option = IntOption(name, default, desc)
        elif valType == ValType.LIST:
            new_option = ListOption(name, default, desc)
        elif valType == ValType.STR:
            new_option = StrOption(name, default, desc)
        else:
            raise OptionzError("uncaught bad option type %d" % valType)

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

    def __init__(clz, name, valType, default, desc):
        clz._name = name
        clz._type = valType
        clz._default = default
        clz._desc = desc       # brief, used in usage()

    @property
    def name(self): return self._name

    @property
    def default(self): return self._default

    @property
    def desc(self): return self._desc


class BoolOption(ZOption):

    def __init__(self, name, default=False, desc=None):
        super().__init__(name, ValType.BOOL, default, desc)

    def __eq__(self, other):
        return  isinstance(other, BoolOption)       and \
            self._name == other.name               and \
            self._default == other.default         and \
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

        if default and not default in choices:
            raise OptionzError("default value '%s' is not in %s's choices" % (
                default, name))

    @property
    def choices(self):
        """ returns a copy of the list of choices """
        return [ch for ch in self._choices]

    def __eq__(self, other):
        return  isinstance(other, ChoiceOption)     and \
            self._name == other.name       and \
            self._default == other.default    and \
            self._desc == other.desc


class FloatOption(ZOption):

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.FLOAT, default, desc)

    def __eq__(self, other):
        return  isinstance(other, FloatOption)      and \
            self._name == other.name       and \
            self._default == other.default    and \
            self._desc == other.desc


class IntOption(ZOption):

    """ Basic attributes of an Option: name, type, default, desc."""

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.INT, default, desc)

    def __eq__(self, other):
        return  isinstance(other, IntOption)      and \
            self._name == other.name       and \
            self._default == other.default    and \
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
    def size(self): return self._default

    def __eq__(self, other):
        return  isinstance(other, ListOption)       and \
            self._name == other.name       and \
            self._default == other.default    and \
            self._desc == other.desc


class StrOption(ZOption):

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.STR, default, desc)

    def __eq__(self, other):
        return  isinstance(other, StrOption)      and \
            self._name == other.name       and \
            self._default == other.default    and \
            self._desc == other.desc
