# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import freepybox

setup(
    name='freepybox',
    version=freepybox.__version__,
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
