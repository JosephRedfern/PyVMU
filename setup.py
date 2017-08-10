#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PyVMU',
    version='0.1.dev1',
    description='Python Toolkit for the Variense VMU931.',
    author='Joseph Redfern',
    author_email='joseph@redfern.me',
    url='https://github.com/JosephRedfern/PyVMU',
    license='MIT',
    platforms=['any'],
    install_requires=[
        'pyserial',
    ],
    packages=['pyvmu'],
)
