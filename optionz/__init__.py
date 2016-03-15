# optionz/optionz/__init__.py

__all__ = [ '__version__', '__version_date__',
            # classes
            'Optionz', 
            'ZOption',   'BoolOption',  'ChoiceOption', 'FloatOption',  
            'IntOption', 'ListOption',  'StrOption',
          ]

__version__      = '0.1.1'
__version_date__ = '2016-03-15'

class Optionz (object):
    O_BOOL      = 1
    O_CHOICE    = 2
    O_FLOAT     = 3
    O_INT       = 4
    O_LIST      = 5
    O_STR       = 6

    def __init__(self, name, desc=None, epilog=None):
        self._name      = name
        self._desc      = desc          # shorter, used in usage()
        self._epilog    = epilog        # shorter, used in usage()
        self._zOptions  = []
        self._zMap      = {}

    @property
    def name(self):         return self._name
    @property
    def desc(self):         return self._desc
    @property
    def epilog(self):       return self._epilog

    # Possibly want to add 'def addChoiceOption()' and 'def addListOption'
    # to handle additional parameters

    def addOption(self, name, valType, default=None, desc=None):
        if valType < self.O_BOOL or valType > self.O_STR:
            raise RuntimeError('unrecognized valType %d', valType)
        if name in self._zOptions:
            raise RuntimeError("duplicate option name '%s'" % name)

        if valType   == self.O_BOOL:
            newOption = BoolOption(name,    desc, default)
        elif valType == ChoiceOption:
            newOption = ChoiceOption(name,  desc, default)
        elif valType == FloatOption:
            newOption = FloatOption(name,   desc, default)
        elif valType == IntOption:
            newOption = IntOption(name,     desc, default)
        elif valType == ListOption:
            newOption = ListOption(name,    desc, default)
        elif valType == StrOption:
            newOption = StrOption(name,     desc, default)
        else:
            raise RuntimeError("uncaught bad option type %d" % valType)

        self._zMap[name] = newOption
        self._zOptions.append(newOption)

    def __len__(self):
        return len(self._zOptions)



class ZOption(object):

    def __init__(clz, name, valType, default, desc):
        clz._name       = name
        clz._type       = valType
        clz._default    = default
        clz._desc       = desc       # brief, used in usage()

    @property
    def name(self):         return self._name
    @property
    def default(self):      return self._default
    @property
    def desc(self):  return self._desc

class BoolOption(ZOption):
    
    def __init__(self, name, default=False, desc=None):
        super().__init__(name, Optionz.O_BOOL, default, desc)

class ChoiceOption(ZOption):
    """ 
    This implementation makes no attempt to make sure that the list
    of choices is homogeneous (all elements are of the same type) or
    otherwise sensible.
    """
    def __init__(self, name, choices, default=None, desc=None):
        super().__init__( name, Optionz.O_CHOICE, default, desc)
        self._choices  = [ch for ch in choices]

        if default and not default in choices:
            raise RuntimeError("default value '%s' is not in %s's choices" % (
                default, name))

    @property
    def choices(self):
        return [ch for ch in self._choices]

class FloatOption(ZOption):
    def __init__(self, name, default=None, desc=None):
        super().__init__( name, Optionz.O_FLOAT, default, desc)

class IntOption(ZOption):
    def __init__(self, name, default=None, desc=None):
        super().__init__( name, Optionz.O_INT, default, desc)


class ListOption(ZOption):
    """
    Here 'default' is interpreted as the number of elements in the
    list: 0 means any number, -N means up to N values inclusive
    may be supplied, and N > 0 means that exactly N values must
    be supplied.
    """
    def __init__(self, name, default=None, desc=None):
        super().__init__( name, Optionz.O_LIST, default, desc)

    # perhaps temporarily:
    @property
    def size(self):         return self._default

class StrOption(ZOption):
    def __init__(self, name, default=None, desc=None):
        super().__init__( name, Optionz.O_STR, default, desc)




