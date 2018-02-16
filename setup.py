# -*- coding: utf-8 -*-

import codecs
import os
import re
from setuptools import setup, find_packages


# Method for retrieving the version is taken from the setup.py of pip itself:
# https://github.com/pypa/pip/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='freepybox',
    version=find_version("freepybox", "__init__.py"),
    packages=find_packages(),
    author='fstercq',
    author_email='',
    description='Provides authentication and row access to Freebox using OS developer API',
    long_description=open('README.md').read(),
    install_requires=['requests'],
    include_package_data=True,
    url='https://github.com/fstercq/freepybox',
    keywords='freebox',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
