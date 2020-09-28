#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: guolong<565169745@qq.com>
from distutils.core import setup
import setuptools
from dbfaker.utils.constant import __version__, __author__, __description__, __author_email__, __url__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='dbfaker',
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
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
		'DBUtils'
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
