#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Benjamin Grewell",
    author_email='benjamin.grewell@intel.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="WEMO Python Wrapper is a simple wrapper around the WEMO gRPC code that simplifies the usage",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wemopy',
    name='wemopy',
    packages=find_packages(include=['wemopy', 'wemopy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bengrewell/wemopy',
    version='0.2.0',
    zip_safe=False,
)
