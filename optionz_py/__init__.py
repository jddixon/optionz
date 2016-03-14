# optionz_py/optionz_py/__init__.py

__all__ = [ '__version__', '__version_date__',
            # classes
            'Optionz',      'ZOption',   'BoolOption',  'ChoiceOption',
            'FloatOption',  'IntOption', 'ListOption',  'StrOption',
          ]

__version__      = '0.0.2'
__version_date__ = '2016-03-14'

class Optionz (object):
    O_BOOL      = 1
    O_CHOICE    = 2
    O_FLOAT     = 3
    O_INT       = 4
    O_LIST      = 5
    O_STR       = 6

    def __init__(self, name, description=None, epilog=None):
        self._name      = name
        self._desc      = description       # shorter, used in usage()
        self._epilog    = epilog            # shorter, used in usage()
        self._zOptions  = []
        self._zMap      = {}

    @property
    def name(self):         return self._name
    @property
    def description(self):  return self._desc
    @property
    def epilog(self):       return self._epilog

    # Possibly want to add 'def addChoiceOption()' and 'def addListOption'
    # to handle additional parameters

    def addOption(self, name, valType, description, default=None):
        if valType < O_BOOL or valType > O_STR:
            raise RuntimeError('unrecognized valType %d', valType)
        if name in self._zoptions:
            raise RuntimeError("duplicate option name '%s'" % name)
        if valType   == O_BOOL:
            newOption = BoolOption(name, default, description)
        elif valType == ChoiceOption:
            newOption = ChoiceOption(name, default, description)
        elif valType == FloatOption:
            newOption = FloatOption(name, default, description)
        elif valType == IntOption:
            newOption = IntOption(name, default, description)
        elif valType == ListOption:
            newOption = ListOption(name, default, description)
        elif valType == StrOption:
            newOption = StrOption(name, default, description)
        else:
            raise RuntimeError("uncaught bad option type %d" % valType)

        self._zMap[name] = newOption
        self._zOptions.append(newOption)

    def __len__(self):
        return len(self._zOptions)


class ZOption(object):

    def __init__(clz, name, valType, description):
        clz._name      = name
        clz._type      = valType
        clz._desc      = description       # brief, used in usage()

class BoolOption(ZOption):
    
    def __init__(self, name, default=False, description=None):
        super().__init__(name, Optionz.O_BOOL, description)
        self._default  = default

    @property
    def name(self):         return self._name
    @property
    def default(self):         return self._default
    @property
    def description(self):  return self._desc

class ChoiceOption(ZOption):
    def __init__(self, name, default=None, description=None):
        super.__init__(self, name, Options.O_CHOICE, description)
        self._default  = default

class FloatOption(ZOption):
    def __init__(self, name, default=None, description=None):
        super.__init__(self, name, Options.O_FLOAT, description)
        self._default  = default

class IntOption(ZOption):
    def __init__(self, name, default=None, description=None):
        super.__init__(self, name, Options.O_INT, description)
        self._default  = default

class ListOption(ZOption):
    def __init__(self, name, default=None, description=None):
        super.__init__(self, name, Options.O_LIST, description)
        self._default  = default

class StrOption(ZOption):
    def __init__(self, name, default=None, description=None):
        super.__init__(self, name, Options.O_STR, description)
        self._default  = default


