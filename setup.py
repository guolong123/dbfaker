#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: guolong<565169745@qq.com>
from distutils.core import setup
import setuptools
import os
import codecs
import re

DESCRIPTION = ''
AUTHOR = ''
URL = ''
VERSION = ''
EMAIL_URL = ''

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), encoding='utf-8').read()


def find_config(*file_paths):
    config_file = read(*file_paths)
    global VERSION, DESCRIPTION, URL, AUTHOR, EMAIL_URL
    VERSION = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                        config_file, re.M).group(1)
    DESCRIPTION = re.search(r"^__description__ = ['\"]([^'\"]*)['\"]",
                            config_file, re.M).group(1)
    AUTHOR = re.search(r"^__author__ = ['\"]([^'\"]*)['\"]",
                       config_file, re.M).group(1)
    URL = re.search(r"^__url__ = ['\"]([^'\"]*)['\"]",
                    config_file, re.M).group(1)
    EMAIL_URL = re.search(r"^__author_email__ = ['\"]([^'\"]*)['\"]",
                    config_file, re.M).group(1)


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

find_config('dbfaker/utils/constant.py')

setup(
    name='dbfaker',
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL_URL,
    url=URL,
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={'console_scripts': [
        'dbfaker = dbfaker.cli:run',
        'table2yml = dbfaker.table2yml:main'
    ]},
    install_requires=[
        'PyMySQL',
        'PyYAML',
        'pypinyin',
        'Faker',
        'Jinja2',
        'SQLAlchemy',
        'ply',
        'tqdm',
        'dbutils'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
