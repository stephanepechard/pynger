# -*- coding: utf-8 -*-
""" pynger setup.py script """

# pynger
from pynger import __version__

# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name='pynger',
    version=__version__,
    description='My pynger project',
    author='Stéphane Péchard',
    author_email='stephanepechard@gmail.com',
    packages=['pynger','pynger.test'],
    url='http://stephanepechard.github.com/pynger',
    long_description=open('README.txt').read(),
    scripts=['bin/pynger'],
    install_requires=['celery', 'jsonschema', 'redis', 'requests'],
    #tests_require=['nose'],
    #test_suite='pynger.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
      ],
)
