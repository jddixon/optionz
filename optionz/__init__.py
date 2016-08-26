#!/usr/bin/env python3

import enum

# optionz/optionz/__init__.py

__all__ = ['__version__', '__version_date__',
           # functions
           'optionzMaker',
           # classes
           'Singleton', 'MetaOption',
           # PROVISIONAL:
           'Optionz', 'ValType',
           'ZOption', 'BoolOption', 'ChoiceOption', 'FloatOption',
           'IntOption', 'ListOption', 'StrOption',
           ]

__version__ = '0.1.14'
__version_date__ = '2016-08-26'


class Singleton(type):
    """
    Classes derived from this metaclass will indeed be singletons.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls is Singleton._instance:
            Singleton._instance = cls
        return Singleton._instance


class Immutable(object):

    def __setattr__(self, name, value):
        raise AttributeError("attempt to change immutable value")


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
        Clz = super().__new__(cls, name, bases, namespace)
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


def optionzMaker(**kwargs):
    class MyOptions(Singleton, metaclass=MetaOption, **kwargs):
        pass
    return MyOptions

#####################################################################
# XXX EVEN MORE PROVISIONAL XXX
#####################################################################


class _BaseOption(object):

    pass


class Option(_BaseOption):

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not other or not isinstance(other, _BaseOption):
            return False

        # DEBUG
        print("eq:")
        print("  self:  %s" % self.__dict__)
        print("  other: %s" % other.__dict__)
        # END
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    __hash__ = None         # since we have defined __eq__

    def __contains__(self, key):
        return key in self.__dict__

# XXX END EVEN MORE PROVISIONAL #####################################


class ValType(enum.IntEnum):
    BOOL = 1
    CHOICE = 2
    FLOAT = 3
    INT = 4
    LIST = 5
    STR = 6


class Optionz (object):

    def __init__(self, name, desc=None, epilog=None):
        self._name = name
        self._desc = desc           # short, top of help message
        self._epilog = epilog       # footer for help message
        self._zOptions = []
        self._zMap = {}

    @property
    def name(self): return self._name

    @property
    def desc(self): return self._desc

    @property
    def epilog(self): return self._epilog

    # Possibly want to add 'def addChoiceOption()' and 'def addListOption'
    # to handle additional parameters

    def addOption(self, name, valType, default=None, desc=None):
        if valType < ValType.BOOL or valType > ValType.STR:
            raise RuntimeError('unrecognized valType %d', valType)
        if name in self._zMap:
            raise ValueError("duplicate option name '%s'" % name)

        if valType == ValType.BOOL:
            newOption = BoolOption(name, default, desc)
        elif valType == ValType.FLOAT:
            newOption = FloatOption(name, default, desc)
        elif valType == ValType.INT:
            newOption = IntOption(name, default, desc)
        elif valType == ValType.LIST:
            newOption = ListOption(name, default, desc)
        elif valType == ValType.STR:
            newOption = StrOption(name, default, desc)
        else:
            raise RuntimeError("uncaught bad option type %d" % valType)

        self._zMap[name] = newOption
        self._zOptions.append(newOption)
        return newOption

    def addChoiceOption(self, name, choices, default=None, desc=None):
        if name in self._zMap:
            raise ValueError("duplicate option name '%s'" % name)
        newOption = ChoiceOption(name, choices, default, desc)
        self._zMap[name] = newOption
        self._zOptions.append(newOption)
        return newOption

    def __len__(self):
        return len(self._zOptions)


class ZOption(object):

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
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc


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
            raise RuntimeError("default value '%s' is not in %s's choices" % (
                default, name))

    @property
    def choices(self):
        """ returns a copy of the list of choices """
        return [ch for ch in self._choices]

    def __eq__(self, other):
        return  isinstance(other, ChoiceOption)     and \
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc


class FloatOption(ZOption):

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.FLOAT, default, desc)

    def __eq__(self, other):
        return  isinstance(other, FloatOption)      and \
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc


class IntOption(ZOption):

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.INT, default, desc)

    def __eq__(self, other):
        return  isinstance(other, IntOption)      and \
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc


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
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc


class StrOption(ZOption):

    def __init__(self, name, default=None, desc=None):
        super().__init__(name, ValType.STR, default, desc)

    def __eq__(self, other):
        return  isinstance(other, StrOption)      and \
            self._name     == other._name       and \
            self._default  == other._default    and \
            self._desc == other._desc
