#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: guolong<565169745@qq.com>
from distutils.core import setup
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dbfaker',
    version='0.0.2-beta0925',
    description='基于数据库层面批量生成有逻辑关联的数据',
    author='Long Guo',
    author_email='565169745@qq.com',
    url='https://gitee.com/guojongg/dbfaker',
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    # scripts=['bin/dbfaker', 'bin/table2yml',],
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
        'ply'

    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Operating System :: OS Independent'
        # 'Intended Audience :: Developers',
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
