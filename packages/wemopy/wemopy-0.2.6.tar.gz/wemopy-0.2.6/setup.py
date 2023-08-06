#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'attrs==21.2.0',
'beautifulsoup4==4.9.3',
'bleach==4.0.0',
'build==0.6.0.post1',
'bump2version==1.0.1',
'certifi==2021.5.30',
'cffi==1.14.6',
'charset-normalizer==2.0.4',
'colorama==0.4.4',
'cryptography==3.4.7',
'docutils==0.17.1',
'google==3.0.0',
'grpcio==1.39.0',
'grpcio-tools==1.39.0',
'idna==3.2',
'importlib-metadata==4.6.3',
'iniconfig==1.1.1',
'jeepney==0.7.1',
'keyring==23.0.1',
'packaging==21.0',
'pep517==0.11.0',
'pkg_resources==0.0.0',
'pkginfo==1.7.1',
'pluggy==0.13.1',
'protobuf==3.17.3',
'py==1.10.0',
'pycparser==2.20',
'Pygments==2.9.0',
'pyparsing==2.4.7',
'pytest==6.2.4',
'readme-renderer==29.0',
'requests==2.26.0',
'requests-toolbelt==0.9.1',
'rfc3986==1.5.0',
'SecretStorage==3.3.1',
'six==1.16.0',
'soupsieve==2.2.1',
'toml==0.10.2',
'tomli==1.2.1',
'tqdm==4.62.0',
'twine==3.4.2',
'typing-extensions==3.10.0.0',
'urllib3==1.26.6',
'webencodings==0.5.1',
'zipp==3.5.0', ]

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
    version='0.2.6',
    zip_safe=False,
)
