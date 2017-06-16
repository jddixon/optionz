#!/usr/bin/python3
# optionz/optionz/setup.py

""" Set up the optionz package. """

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('src/optionz/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='optionz',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      # list packages in separate directories
      packages=['src/optionz', ],
      # following could be in scripts/ subdir
      scripts=[],
      description='command line options processor',
      url='https://jddixon.github.io/optionz',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          "Development Status :: 2 - Pre-Alpha",
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python 3',
      ],)
