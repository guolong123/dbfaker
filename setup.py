#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: guolong<565169745@qq.com>
from distutils.core import setup
import setuptools

setup(
    name='dbfaker',  # 包的名字
    version='0.0.1',  # 版本号
    description='基于数据库层面批量生成有逻辑关联的数据',  # 描述
    author='Long Guo',  # 作者
    author_email='565169745@qq.com',  # 你的邮箱**
    url='https://gitee.com/565169745/dbfaker',  # 可以写github上的地址，或者其他地址
    packages=setuptools.find_packages(),  # 包内需要引用的文件夹

    # 依赖包
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
        'Operating System :: Microsoft'  # 你的操作系统
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
