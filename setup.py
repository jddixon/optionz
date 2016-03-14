#!/usr/bin/python3

# optionz_py/optionz_py/setup.py

import re
from distutils.core import setup
__version__ = re.search("__version__\s*=\s*'(.*)'",
                    open('optionz_py/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup ( name         = 'optionz_py', 
        version      = __version__,
        author       = 'Jim Dixon',
        author_email = 'jddixon@gmail.com',
        py_modules   = [ ],
        packages     = ['optionz_py'], 
        # following could be in scripts/ subdir
        scripts      = [],
        # MISSING url
        )
