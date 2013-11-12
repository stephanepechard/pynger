# -*- coding: utf-8 -*-
""" pyng setup.py script """

# pyng
from pyng import __version__

# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name='pyng',
    version=__version__,
    description='My pyng project',
    author='Stéphane Péchard',
    author_email='stephanepechard@gmail.com',
    packages=['pyng','pyng.test'],
    url='http://stephanepechard.github.com/pyng',
    long_description=open('README.txt').read(),
    scripts=['bin/pyng'],
    install_requires=['celery', 'redis', 'requests'],
    #tests_require=['nose'],
    #test_suite='pyng.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
      ],
)
